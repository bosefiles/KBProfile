import socket
from datetime import datetime
from typing import Dict

import whois

from osnit.services.provider import OSINTProvider


class LocalProvider(OSINTProvider):
    name = "local-python"

    async def ip_lookup(self, ip: str) -> Dict[str, object]:
        try:
            host, aliases, addresses = socket.gethostbyaddr(ip)
        except Exception:
            host, aliases, addresses = "unknown", [], []

        return {
            "ip": ip,
            "reverse_dns": host,
            "aliases": aliases,
            "addresses": addresses,
            "looked_up_at": datetime.utcnow().isoformat(),
        }

    async def dns_lookup(self, domain: str) -> Dict[str, object]:
        records = {}
        try:
            records["a"] = socket.gethostbyname_ex(domain)[2]
        except Exception:
            records["a"] = []

        try:
            records["mx"] = [
                answer[1]
                for answer in socket.getaddrinfo(f"mail.{domain}", 25, proto=socket.IPPROTO_TCP)
            ]
        except Exception:
            records["mx"] = []

        return {
            "domain": domain,
            "records": records,
            "looked_up_at": datetime.utcnow().isoformat(),
        }

    async def whois_lookup(self, domain: str) -> Dict[str, object]:
        result = whois.whois(domain)
        normalized = dict(result)
        for key, value in normalized.items():
            if isinstance(value, datetime):
                normalized[key] = value.isoformat()
            elif isinstance(value, list):
                normalized[key] = [v.isoformat() if isinstance(v, datetime) else v for v in value]

        return {
            "domain": domain,
            "whois": normalized,
            "looked_up_at": datetime.utcnow().isoformat(),
        }
