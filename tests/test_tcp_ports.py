import pytest
import allure
from engines.tcp_engine import check_tcp_port

@pytest.mark.tcp
@allure.epic("Network Health Validations")
@allure.feature("Layer 4 - Transport")
@allure.story("TCP Protocol Connectivity")
class TestTCPPorts:

    @allure.title("Verify TCP Port is Open and Responsive")
    @allure.description("Performs a TCP 3-way handshake and verifies the port is open and responds within the configured timeout.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tcp_connectivity(self, tcp_target):
        host = tcp_target["host"]
        port = tcp_target["port"]
        timeout = tcp_target["timeout"]
        expect_success = tcp_target["expect_success"]

        with allure.step(f"Initiating TCP handshake to {host} on port {port}"):
            result = check_tcp_port(host, port, timeout)

        with allure.step(f"Validating connection (Expected Success: {expect_success})"):
            if expect_success:
                assert result["success"] is True, f"TCP Connection to {host}:{port} failed. Error: {result['error']}"
                allure.attach(str(result["latency_ms"]), name="Latency (ms)", attachment_type=allure.attachment_type.TEXT)
                assert result["latency_ms"] < 500, "Latency is too high!"
            else:
                assert result["success"] is False, f"Negative Test Failed: Expected connection to {host}:{port} to fail, but it succeeded!"
