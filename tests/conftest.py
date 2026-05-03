import yaml
import pytest
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "targets.yaml"

def load_targets():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return data.get("targets", [])

def get_tcp_test_cases():
    targets = load_targets()
    test_cases = []
    for target in targets:
        for port in target.get("tcp_ports", []):
            test_cases.append({
                "name": target["name"],
                "host": target["host"],
                "port": port,
                "timeout": target.get("timeout_sec", 2),
                "expect_success": target.get("expect_success", True)
            })
    return test_cases

@pytest.fixture(params=get_tcp_test_cases(), ids=lambda tc: f"{tc['name']}:{tc['port']}")
def tcp_target(request):
    return request.param

def get_dns_test_cases():
    targets = load_targets()
    dns_cases = []
    for target in targets:
        # heuristic: entries with letters in host are domain names, not raw IPs
        if any(c.isalpha() for c in target["host"]):
            dns_cases.append({
                "name": target["name"],
                "host": target["host"],
                "expect_success": target.get("expect_success", True)
            })
    return dns_cases

@pytest.fixture(params=get_dns_test_cases(), ids=lambda tc: tc['name'])
def dns_target(request):
    return request.param

def get_http_test_cases():
    targets = load_targets()
    http_cases = []
    for target in targets:
        if "url" in target:
            http_cases.append({
                "name": target["name"],
                "host": target["host"],
                "url": target["url"],
                "check_tls": target.get("check_tls", False),
                "timeout": target.get("timeout_sec", 3),
                "expect_success": target.get("expect_success", True)
            })
    return http_cases

@pytest.fixture(params=get_http_test_cases(), ids=lambda tc: tc['name'])
def http_target(request):
    return request.param
