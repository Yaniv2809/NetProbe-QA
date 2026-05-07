# NetProbe-QA

Automated Network Health & Protocol Validation Framework built with Python and pytest.

Validates DNS resolution, TCP port connectivity, and HTTP/HTTPS status (including TLS certificate expiry) against a YAML-defined target list. Every test is tagged by OSI layer and produces an Allure report with severity levels. Runs in CI/CD via GitHub Actions.

---

## Architecture

```
config/
  targets.yaml         # target definitions (hosts, ports, URLs)
engines/
  dns_engine.py        # DNS A-record resolution + NXDOMAIN detection
  tcp_engine.py        # TCP 3-way handshake connectivity check
  http_engine.py       # HTTP status + TLS certificate expiry
tests/
  conftest.py          # YAML-driven parametrization fixtures
  test_dns_health.py
  test_tcp_ports.py
  test_http_health.py
.github/
  workflows/ci.yml     # GitHub Actions CI pipeline
```

---

## Quick Start

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

pytest tests/ -v
```

### With Allure report

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run a specific OSI layer

```bash
pytest tests/ -m dns
pytest tests/ -m tcp
pytest tests/ -m http
```

---

## Configuration

Edit `config/targets.yaml` to define your targets:

```yaml
targets:
  - name: "My Server"
    host: "example.com"
    tcp_ports: [80, 443]
    url: "https://example.com"
    check_tls: true
    timeout_sec: 3
    expect_success: true
```

| Field | Type | Description |
|---|---|---|
| `name` | string | Display name used in test IDs and reports |
| `host` | string | Domain name or IP address |
| `tcp_ports` | list | Ports to validate via TCP handshake |
| `url` | string | *(optional)* URL for HTTP GET check |
| `check_tls` | bool | *(optional)* Validate TLS certificate expiry |
| `timeout_sec` | int | Connection timeout in seconds |
| `expect_success` | bool | Set `false` to run as a negative test |

---

## Test Coverage

| Test | Protocol | OSI Layer | Validates |
|---|---|---|---|
| `test_dns_resolution` | DNS | L7 | A-record lookup, NXDOMAIN handling |
| `test_tcp_connectivity` | TCP | L4 | 3-way handshake, port reachability, latency < 500ms |
| `test_http_status` | HTTP/HTTPS | L7 | Status 200, connection errors |
| `test_tls_certificate` | TLS | L7 | Certificate validity, ≥ 30 days to expiry |

Both positive and negative test paths are supported via `expect_success` in the YAML config.

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs the full test suite on every push and pull request. Allure results are uploaded as a build artifact.

---

## Requirements

- Python 3.10+
- No external networking tools required — uses Python's standard library (`socket`, `ssl`, `urllib`) with `pytest` and `allure-pytest`

