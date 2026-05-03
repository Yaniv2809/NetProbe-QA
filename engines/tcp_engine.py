import socket
import time

def check_tcp_port(host: str, port: int, timeout: int = 2) -> dict:
    start_time = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            latency = (time.time() - start_time) * 1000
            return {
                "success": True,
                "latency_ms": round(latency, 2),
                "error": None
            }
        except socket.timeout:
            return {
                "success": False,
                "latency_ms": None,
                "error": "Connection Timeout"
            }
        except ConnectionRefusedError:
            return {
                "success": False,
                "latency_ms": None,
                "error": "Connection Refused (Port is closed)"
            }
        except Exception as e:
            return {
                "success": False,
                "latency_ms": None,
                "error": str(e)
            }
