from fastapi import APIRouter

from osnit.core.models import (
    DNSRequest,
    IndiaFootprintSnapshot,
    IndiaFootprintSource,
    IPLookupRequest,
    IntelligenceRecord,
    PortScanRequest,
    PortScanResult,
    WhoisRequest,
)
from osnit.services.india_footprint import IndiaFootprintRepository
from osnit.services.local_provider import LocalProvider
from osnit.services.portscan import scan_ports

router = APIRouter()
provider = LocalProvider()
india_repository = IndiaFootprintRepository()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "osnit"}


@router.post("/lookup/ip", response_model=IntelligenceRecord)
async def lookup_ip(payload: IPLookupRequest) -> IntelligenceRecord:
    data = await provider.ip_lookup(payload.ip)
    return IntelligenceRecord(indicator=payload.ip, kind="ip", data=data, provider=provider.name)


@router.post("/lookup/dns", response_model=IntelligenceRecord)
async def lookup_dns(payload: DNSRequest) -> IntelligenceRecord:
    data = await provider.dns_lookup(payload.domain)
    return IntelligenceRecord(indicator=payload.domain, kind="dns", data=data, provider=provider.name)


@router.post("/lookup/whois", response_model=IntelligenceRecord)
async def lookup_whois(payload: WhoisRequest) -> IntelligenceRecord:
    data = await provider.whois_lookup(payload.domain)
    return IntelligenceRecord(indicator=payload.domain, kind="whois", data=data, provider=provider.name)


@router.post("/scan/ports", response_model=PortScanResult)
async def port_scan(payload: PortScanRequest) -> PortScanResult:
    open_ports, closed_ports = await scan_ports(payload.host, payload.ports, payload.timeout)
    return PortScanResult(host=payload.host, open_ports=open_ports, closed_ports=closed_ports)


@router.get("/india/sources", response_model=list[IndiaFootprintSource])
async def list_india_sources() -> list[IndiaFootprintSource]:
    return india_repository.sources()


@router.post("/india/snapshot/refresh", response_model=IndiaFootprintSnapshot)
async def refresh_india_snapshot() -> IndiaFootprintSnapshot:
    return await india_repository.refresh_snapshot()


@router.get("/india/snapshot/latest", response_model=IndiaFootprintSnapshot)
async def get_latest_india_snapshot() -> IndiaFootprintSnapshot:
    snapshot = india_repository.latest_snapshot()
    if snapshot is None:
        return await india_repository.refresh_snapshot()
    return snapshot
