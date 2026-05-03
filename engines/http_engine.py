import urllib.request
import urllib.error
import ssl
import socket
from datetime import datetime, timezone

def check_http_status(url: str, timeout: int = 3) -> dict:
    try:
        response = urllib.request.urlopen(url, timeout=timeout)
        return {
            "success": True,
            "status_code": response.getcode(),
            "error": None
        }
    except urllib.error.HTTPError as e:
        return {"success": False, "status_code": e.code, "error": f"HTTP Error: {e.code}"}
    except Exception as e:
        return {"success": False, "status_code": None, "error": str(e)}

def check_tls_expiry(host: str, port: int = 443, timeout: int = 3) -> dict:
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        current_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        days_left = (expire_date - current_utc).days

        return {
            "success": True,
            "days_left": days_left,
            "error": None
        }
    except ssl.SSLCertVerificationError as e:
        return {"success": False, "days_left": None, "error": f"Cert Verification Failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "days_left": None, "error": str(e)}
