import pytest
import allure
from engines.dns_engine import resolve_dns

@pytest.mark.dns
@allure.epic("Network Health Validations")
@allure.feature("Layer 7 - Application")
@allure.story("DNS Protocol Resolution")
class TestDNSHealth:

    @allure.title("Verify Domain Name Resolution (A Record)")
    @allure.description("Performs a DNS query and verifies the domain resolves to a valid IP, or fails with NXDOMAIN for an invalid domain.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_dns_resolution(self, dns_target):
        domain = dns_target["host"]
        expect_success = dns_target["expect_success"]

        with allure.step(f"Initiating DNS query for domain: {domain}"):
            result = resolve_dns(domain)

        with allure.step(f"Validating DNS response (Expected Success: {expect_success})"):
            if expect_success:
                assert result["success"] is True, f"DNS Resolution for {domain} failed. Error: {result['error']}"
                allure.attach(f"Resolved IP: {result['ip']}", name="DNS Result", attachment_type=allure.attachment_type.TEXT)
            else:
                assert result["success"] is False, f"Negative Test Failed: Expected DNS resolution for {domain} to fail, but it resolved to {result['ip']}!"
