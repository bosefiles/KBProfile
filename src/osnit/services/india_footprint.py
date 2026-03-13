from __future__ import annotations

import asyncio
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import httpx

from osnit.core.models import IndiaFootprintSnapshot, IndiaFootprintSource, IndiaFootprintSourceResult


@dataclass(frozen=True)
class SourceDefinition:
    source_id: str
    name: str
    category: str
    url: str
    description: str
    format_hint: str


class IndiaFootprintRepository:
    """Collects and categorizes open India-focused digital footprint datasets."""

    def __init__(self, base_dir: str = "data/india_open_footprints") -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.history_path = self.base_path / "history"
        self.history_path.mkdir(parents=True, exist_ok=True)
        self.latest_path = self.base_path / "latest.json"

        self._sources: list[SourceDefinition] = [
            SourceDefinition(
                source_id="in_states_geojson",
                name="India State Boundaries",
                category="geospatial",
                url="https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson",
                description="Open state boundary data for map-based study and regional overlays.",
                format_hint="geojson",
            ),
            SourceDefinition(
                source_id="in_districts_geojson",
                name="India District Boundaries",
                category="geospatial",
                url="https://raw.githubusercontent.com/datameet/maps/master/Districts/india_district.geojson",
                description="District-level shapes for granular pan-India comparisons.",
                format_hint="geojson",
            ),
            SourceDefinition(
                source_id="in_rail_stations",
                name="Indian Railways Station Master",
                category="mobility",
                url="https://raw.githubusercontent.com/datameet/railways/master/stations.csv",
                description="Open station records useful for transport footprint analysis.",
                format_hint="csv",
            ),
            SourceDefinition(
                source_id="in_air_quality_cpcb",
                name="CPCB Open AQ Feed",
                category="environment",
                url="https://api.openaq.org/v3/locations?countries=IN&limit=100",
                description="Air-quality monitoring locations across India.",
                format_hint="json",
            ),
            SourceDefinition(
                source_id="in_earthquakes_usgs",
                name="USGS India Earthquake Window",
                category="hazard",
                url="https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2024-01-01&minlatitude=6&maxlatitude=38&minlongitude=68&maxlongitude=98",
                description="Seismic events over the India region from a public global feed.",
                format_hint="geojson",
            ),
            SourceDefinition(
                source_id="in_certin_advisories",
                name="CERT-In Advisories",
                category="cybersecurity",
                url="https://www.cert-in.org.in/RSS_Feed.jsp",
                description="India cyber advisories and alerts feed.",
                format_hint="xml",
            ),
            SourceDefinition(
                source_id="in_rbi_announcements",
                name="RBI Press Releases",
                category="economy",
                url="https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx",
                description="Macro-finance and policy communication from India's central bank.",
                format_hint="html",
            ),
            SourceDefinition(
                source_id="in_mygov_open_feed",
                name="MyGov India Open RSS",
                category="governance",
                url="https://www.mygov.in/feed/",
                description="Public participation and policy communication feed.",
                format_hint="xml",
            ),
        ]

    def sources(self) -> list[IndiaFootprintSource]:
        return [IndiaFootprintSource(**source.__dict__) for source in self._sources]

    async def _fetch_source(
        self, client: httpx.AsyncClient, source: SourceDefinition
    ) -> IndiaFootprintSourceResult:
        fetched_at = datetime.now(timezone.utc)
        try:
            response = await client.get(source.url)
            payload = response.text
            digest = hashlib.sha256(payload.encode("utf-8", errors="ignore")).hexdigest()
            sample = payload[:240].replace("\n", " ").strip()
            return IndiaFootprintSourceResult(
                source_id=source.source_id,
                category=source.category,
                fetched_at=fetched_at,
                status_code=response.status_code,
                content_type=response.headers.get("content-type", "unknown"),
                content_sha256=digest,
                size_bytes=len(payload.encode("utf-8")),
                sample=sample,
                error=None,
            )
        except Exception as exc:  # noqa: BLE001
            return IndiaFootprintSourceResult(
                source_id=source.source_id,
                category=source.category,
                fetched_at=fetched_at,
                status_code=0,
                content_type="unknown",
                content_sha256="",
                size_bytes=0,
                sample="",
                error=str(exc),
            )

    async def refresh_snapshot(self) -> IndiaFootprintSnapshot:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            results = await asyncio.gather(
                *(self._fetch_source(client, source) for source in self._sources)
            )

        category_counts = dict(Counter(source.category for source in results))
        snapshot = IndiaFootprintSnapshot(
            generated_at=datetime.now(timezone.utc),
            total_sources=len(results),
            category_counts=category_counts,
            sources=results,
        )
        self._persist(snapshot)
        return snapshot

    def _persist(self, snapshot: IndiaFootprintSnapshot) -> None:
        payload = json.dumps(snapshot.model_dump(mode="json"), indent=2)
        self.latest_path.write_text(payload, encoding="utf-8")
        history_file = self.history_path / f"{snapshot.generated_at.strftime('%Y%m%dT%H%M%SZ')}.json"
        history_file.write_text(payload, encoding="utf-8")

    def latest_snapshot(self) -> IndiaFootprintSnapshot | None:
        if not self.latest_path.exists():
            return None
        raw = json.loads(self.latest_path.read_text(encoding="utf-8"))
        return IndiaFootprintSnapshot(**raw)


class IndiaFootprintScheduler:
    def __init__(self, repository: IndiaFootprintRepository, interval_seconds: int = 1800) -> None:
        self.repository = repository
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        if self._task is not None:
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._runner())

    async def stop(self) -> None:
        if self._task is None:
            return
        self._stop_event.set()
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None

    async def _runner(self) -> None:
        while not self._stop_event.is_set():
            await self.repository.refresh_snapshot()
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval_seconds)
            except TimeoutError:
                continue
