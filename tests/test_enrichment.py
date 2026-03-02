import pytest
from unittest.mock import Mock, patch
from enrichment import DataEnrichment
from models import LogLine
from geoip2.errors import AddressNotFoundError

@pytest.fixture
def mock_log_line():
    return LogLine(
        ip_address="8.8.8.8",
        timestamp="10/Oct/2000:13:55:36 -0700",
        request_method="GET",
        request_url="/",
        request_protocol="HTTP/1.0",
        status_code=200,
        response_size=100,
        temp_user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    ).model_copy(update={"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"})

@patch('geoip2.database.Reader')
def test_enrichment_valid_data(mock_reader_class, mock_log_line):
    # Mock GeoIP return
    mock_reader = Mock()
    mock_country = Mock()
    mock_country.country.name = "United States"
    mock_reader.country.return_value = mock_country
    mock_reader_class.return_value = mock_reader

    enricher = DataEnrichment("dummy_db.mmdb")
    enriched_line = enricher.enrich(mock_log_line)

    assert enriched_line.country == "United States"
    assert enriched_line.browser == "Chrome"
    assert enriched_line.os == "Windows"

@patch('geoip2.database.Reader')
def test_enrichment_geoip_not_found(mock_reader_class, mock_log_line):
    mock_reader = Mock()
    mock_reader.country.side_effect = AddressNotFoundError("Not found")
    mock_reader_class.return_value = mock_reader

    enricher = DataEnrichment("dummy_db.mmdb")
    enriched_line = enricher.enrich(mock_log_line)

    assert enriched_line.country == "Unknown"

@patch('geoip2.database.Reader')
def test_enrichment_invalid_user_agent(mock_reader_class):
    mock_reader_class.return_value = Mock()
    
    # Log line with no user agent
    log_line = LogLine(
        ip_address="8.8.8.8",
        timestamp="10/Oct/2000:13:55:36 -0700",
        request_method="GET",
        request_url="/",
        request_protocol="HTTP/1.0",
        status_code=200,
        response_size=100,
        user_agent=None
    )

    enricher = DataEnrichment("dummy_db.mmdb")
    enriched_line = enricher.enrich(log_line)

    assert enriched_line.browser == "Unknown"
    assert enriched_line.os == "Unknown"
