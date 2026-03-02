import pytest
from models import LogLine
from dimensions import (
    CountryDimension,
    BrowserDimension,
    OSDimension
)

@pytest.fixture
def sample_log_line():
    return LogLine(
        ip_address="192.168.1.1",
        user_identifier=None,
        user_id=None,
        timestamp="10/Oct/2000:13:55:36 -0700",
        request_method="GET",
        request_url="/apache_pb.gif?dummy=str",
        request_protocol="HTTP/1.0",
        status_code=200,
        response_size=2326,
        referer=None,
        user_agent="MockBrowser 1.0",
        country="United States",
        browser="MockBrowser 1.0",
        os="MockOS",
    )

def test_country_dimension(sample_log_line):
    dim = CountryDimension()
    assert dim.name == "Country"
    assert dim.extract_data(sample_log_line) == "United States"

def test_browser_dimension(sample_log_line):
    dim = BrowserDimension()
    assert dim.name == "Browser"
    assert dim.extract_data(sample_log_line) == "MockBrowser 1.0"

def test_os_dimension(sample_log_line):
    dim = OSDimension()
    assert dim.name == "OS"
    assert dim.extract_data(sample_log_line) == "MockOS"




