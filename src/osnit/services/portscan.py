import asyncio
from typing import Iterable, List, Tuple


async def scan_port(host: str, port: int, timeout: float) -> Tuple[int, bool]:
    try:
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return port, True
    except Exception:
        return port, False


async def scan_ports(host: str, ports: Iterable[int], timeout: float = 0.5) -> Tuple[List[int], List[int]]:
    tasks = [scan_port(host, port, timeout) for port in ports]
    results = await asyncio.gather(*tasks)

    open_ports = [port for port, is_open in results if is_open]
    closed_ports = [port for port, is_open in results if not is_open]
    return open_ports, closed_ports
