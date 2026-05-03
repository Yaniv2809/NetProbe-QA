import socket
import time

def resolve_dns(domain: str) -> dict:
    start_time = time.time()
    try:
        ip_address = socket.gethostbyname(domain)
        latency = (time.time() - start_time) * 1000
        return {
            "success": True,
            "ip": ip_address,
            "latency_ms": round(latency, 2),
            "error": None
        }
    except socket.gaierror as e:
        return {
            "success": False,
            "ip": None,
            "latency_ms": None,
            "error": f"DNS Resolution Failed (NXDOMAIN): {str(e)}"
        }
