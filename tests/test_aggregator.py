import pytest
from models import LogLine
from aggregator import DataAggregator
from dimensions import OSDimension

@pytest.fixture
def mock_log_windows():
    return LogLine(
        ip_address="1.1.1.1",
        timestamp="10/Oct/2000:13:55:36 -0700",
        request_method="GET",
        request_url="/",
        request_protocol="HTTP/1.0",
        status_code=200,
        response_size=100,
        os="Windows 10"
    )

@pytest.fixture
def mock_log_mac():
    return LogLine(
        ip_address="1.1.1.1",
        timestamp="10/Oct/2000:13:55:36 -0700",
        request_method="GET",
        request_url="/",
        request_protocol="HTTP/1.0",
        status_code=200,
        response_size=100,
        os="Mac OS X"
    )

def test_aggregator_adds_correctly(mock_log_windows, mock_log_mac):
    dim = OSDimension()
    aggregator = DataAggregator(dimension=dim)
    
    # Empty state
    assert len(aggregator.get_results()) == 0

    # Add windows
    aggregator.add(mock_log_windows)
    results = aggregator.get_results()
    assert len(results) == 1
    assert results["Windows 10"] == 1

    # Add Mac
    aggregator.add(mock_log_mac)
    results = aggregator.get_results()
    assert len(results) == 2
    assert results["Windows 10"] == 1
    assert results["Mac OS X"] == 1

    # Add Windows again
    aggregator.add(mock_log_windows)
    results = aggregator.get_results()
    assert len(results) == 2
    assert results["Windows 10"] == 2
    assert results["Mac OS X"] == 1
