import asyncio
from pathlib import Path

from osnit.services.india_footprint import IndiaFootprintRepository


def test_refresh_snapshot_persists(monkeypatch, tmp_path: Path) -> None:
    repo = IndiaFootprintRepository(base_dir=str(tmp_path))

    async def fake_fetch(_client, source):
        from datetime import datetime, timezone

        from osnit.core.models import IndiaFootprintSourceResult

        return IndiaFootprintSourceResult(
            source_id=source.source_id,
            category=source.category,
            fetched_at=datetime.now(timezone.utc),
            status_code=200,
            content_type="application/json",
            content_sha256="abc",
            size_bytes=10,
            sample="ok",
            error=None,
        )

    monkeypatch.setattr(repo, "_fetch_source", fake_fetch)

    snapshot = asyncio.run(repo.refresh_snapshot())

    assert snapshot.total_sources == len(repo.sources())
    assert (tmp_path / "latest.json").exists()
    assert any((tmp_path / "history").iterdir())
