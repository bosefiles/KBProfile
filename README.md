# OSNIT (Python)

OSNIT is a Python-based OSINT application scaffold designed to evolve into a larger analyst platform.

## Features in this MVP

- IP lookup (reverse DNS + metadata)
- DNS lookup (basic A/MX-style hints)
- WHOIS lookup
- Async TCP port scanning
- FastAPI REST API with typed schemas
- Provider abstraction for future integration with external APIs (e.g., HackerTarget API)
- India open digital footprint repository (categorized pan-India source catalog)
- Auto-refresh scheduler every 30 minutes with local snapshot persistence

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn osnit.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Example requests

```bash
curl -X POST http://127.0.0.1:8000/api/v1/lookup/ip \
  -H 'Content-Type: application/json' \
  -d '{"ip":"8.8.8.8"}'

curl -X POST http://127.0.0.1:8000/api/v1/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{"host":"scanme.nmap.org","ports":[22,80,443]}'

curl http://127.0.0.1:8000/api/v1/india/sources

curl -X POST http://127.0.0.1:8000/api/v1/india/snapshot/refresh

curl http://127.0.0.1:8000/api/v1/india/snapshot/latest
```

## India open footprint repository behavior

- The server starts a background scheduler that refreshes India-focused open-source footprint data every **30 minutes**.
- Snapshots are stored in `data/india_open_footprints/latest.json` and timestamped history files in `data/india_open_footprints/history/`.
- Sources are categorized (e.g., governance, environment, economy, geospatial, cybersecurity, mobility, hazard) for easier study.

## Architecture direction for "next Palantir Gotham" style evolution

1. Add ingest pipelines for multiple intel providers.
2. Add graph model (entities: IP, domain, org, person, certificate).
3. Add case workspace + timeline + notebook + link analysis.
4. Add RBAC, audit trails, and immutable evidence snapshots.
5. Add ML-assisted anomaly detection and triage scoring.

## Notes

- This MVP currently uses a local Python provider and is ready for adapter integration with external API specs.
- Only scan infrastructure you are authorized to assess.
