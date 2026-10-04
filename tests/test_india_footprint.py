import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pytest

from osnit.core.models import IndiaFootprintSnapshot
from osnit.services.india_footprint import IndiaFootprintRepository, IndiaFootprintScheduler


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


@pytest.mark.parametrize("concurrent", [False, True])
def test_persist_preserves_snapshots_with_identical_timestamps(
    tmp_path: Path, concurrent: bool
) -> None:
    generated_at = datetime(2026, 3, 13, 4, 0, tzinfo=timezone.utc)
    snapshots = [
        IndiaFootprintSnapshot(
            generated_at=generated_at,
            total_sources=0,
            category_counts={str(index): 0},
            sources=[],
        )
        for index in range(10)
    ]

    def persist(snapshot: IndiaFootprintSnapshot) -> None:
        # Separate instances also exercise writers sharing the same history directory.
        IndiaFootprintRepository(base_dir=str(tmp_path))._persist(snapshot)

    if concurrent:
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(persist, snapshots))
    else:
        for snapshot in snapshots:
            persist(snapshot)
        assert IndiaFootprintRepository(str(tmp_path)).latest_snapshot() == snapshots[-1]

    history_files = list((tmp_path / "history").glob("*.json"))
    assert len(history_files) == len(snapshots)
    saved = [
        IndiaFootprintSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
        for path in history_files
    ]
    assert all(snapshot in saved for snapshot in snapshots)


def test_scheduler_continues_after_interval_timeout(monkeypatch, tmp_path: Path) -> None:
    async def exercise():
        repo = IndiaFootprintRepository(str(tmp_path))
        scheduler = IndiaFootprintScheduler(repo, interval_seconds=0.001)
        refreshed = asyncio.Event()
        calls = 0

        async def refresh():
            nonlocal calls
            calls += 1
            if calls == 3:
                refreshed.set()

        monkeypatch.setattr(repo, "refresh_snapshot", refresh)
        await scheduler.start()
        try:
            await asyncio.wait_for(refreshed.wait(), timeout=2)
            assert calls >= 3
            assert not scheduler._task.done()
        finally:
            await scheduler.stop()
        assert scheduler._task is None

    asyncio.run(exercise())
