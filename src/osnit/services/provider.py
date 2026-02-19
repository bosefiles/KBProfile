from abc import ABC, abstractmethod
from typing import Dict


class OSINTProvider(ABC):
    """Abstract provider so we can swap API providers later (e.g., HackerTarget)."""

    name: str

    @abstractmethod
    async def ip_lookup(self, ip: str) -> Dict[str, object]:
        raise NotImplementedError

    @abstractmethod
    async def dns_lookup(self, domain: str) -> Dict[str, object]:
        raise NotImplementedError

    @abstractmethod
    async def whois_lookup(self, domain: str) -> Dict[str, object]:
        raise NotImplementedError
