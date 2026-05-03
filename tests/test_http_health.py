import pytest
import allure
from engines.http_engine import check_http_status, check_tls_expiry

@pytest.mark.http
@allure.epic("Network Health Validations")
@allure.feature("Layer 7 - Application")
@allure.story("HTTP/HTTPS and TLS Certificates")
class TestHTTPHealth:

    @allure.title("Verify HTTP Status Code is 200 OK")
    @allure.description("Sends an HTTP GET request and verifies the server returns a successful status.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_http_status(self, http_target):
        url = http_target["url"]
        timeout = http_target["timeout"]
        expect_success = http_target["expect_success"]

        with allure.step(f"Sending HTTP GET request to {url}"):
            result = check_http_status(url, timeout)

        with allure.step(f"Validating response (Expected Success: {expect_success})"):
            if expect_success:
                assert result["success"] is True, f"HTTP Request failed. Error: {result['error']}"
                assert result["status_code"] == 200, f"Expected status 200, got {result['status_code']}"
                allure.attach(str(result["status_code"]), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            else:
                assert result["success"] is False, f"Negative Test Failed: Expected HTTP to fail for {url}!"

    @allure.title("Verify TLS Certificate Expiry")
    @allure.description("Retrieves the TLS certificate and verifies it does not expire within the next 30 days.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tls_certificate(self, http_target):
        if not http_target["check_tls"]:
            pytest.skip(f"TLS validation is disabled for {http_target['name']} in targets.yaml")

        host = http_target["host"]
        timeout = http_target["timeout"]

        with allure.step(f"Extracting TLS certificate for {host}"):
            result = check_tls_expiry(host, port=443, timeout=timeout)

        with allure.step("Validating certificate validity period"):
            assert result["success"] is True, f"TLS Extraction failed. Error: {result['error']}"
            days_left = result["days_left"]
            allure.attach(f"{days_left} Days", name="Time to Expiry", attachment_type=allure.attachment_type.TEXT)
            assert days_left > 30, f"SECURITY RISK: TLS Certificate for {host} expires too soon! Only {days_left} days left."
