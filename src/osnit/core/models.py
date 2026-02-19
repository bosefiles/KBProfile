from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class IPLookupRequest(BaseModel):
    ip: str = Field(..., description="IPv4 or IPv6 address")


class WhoisRequest(BaseModel):
    domain: str = Field(..., description="Domain name")


class DNSRequest(BaseModel):
    domain: str = Field(..., description="Domain name")


class PortScanRequest(BaseModel):
    host: str = Field(..., description="Target hostname or IP")
    ports: List[int] = Field(default_factory=lambda: [22, 53, 80, 443, 8080])
    timeout: float = Field(default=0.5, ge=0.1, le=5.0)


class PortScanResult(BaseModel):
    host: str
    open_ports: List[int]
    closed_ports: List[int]


class IntelligenceRecord(BaseModel):
    indicator: str
    kind: str
    data: Dict[str, object]
    provider: str
    note: Optional[str] = None
