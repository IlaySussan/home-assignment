import pytest
from models import LogLine
from parser import DataParser

@pytest.fixture
def parser():
    return DataParser()

def test_data_parser_valid_line(parser):
    line = '83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"'
    log_line = parser.parse_line(line)
    
    assert log_line is not None
    assert log_line.ip_address == "83.149.9.216"
    assert "17/May/2015" in log_line.timestamp
    assert log_line.request_method == "GET"
    assert log_line.status_code == 200
    assert log_line.response_size == 203023
    assert log_line.user_agent.startswith("Mozilla/5.0 (Macintosh")

def test_data_parser_invalid_line(parser):
    line = "This is not a valid apache log line"
    log_line = parser.parse_line(line)
    assert log_line is None

def test_data_parser_missing_size(parser):
    line = '83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 - "-" "-"'
    log_line = parser.parse_line(line)
    
    assert log_line is not None
    assert log_line.response_size == 0
    assert log_line.referer is None
    assert log_line.user_agent is None

def test_data_parser_empty_line(parser):
    assert parser.parse_line("") is None
    assert parser.parse_line("   \n") is None

def test_data_parser_malformed_request_line(parser):
    # Missing protocol and URL partly
    line = '83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET" 400 0 "-" "-"'
    log_line = parser.parse_line(line)
    assert log_line is not None
    assert log_line.request_method == "GET"
    assert log_line.request_url == "-"
    assert log_line.request_protocol == "-"

def test_data_parser_weird_status(parser):
    # Apache allows non-integer status codes in some absolutely malformed setups but regex expects \d{3}
    line = '83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET / HTTP/1.1" ABC 0 "-" "-"'
    log_line = parser.parse_line(line)
    assert log_line is None

def test_data_parser_truncated_user_agent(parser):
    # Log line missing the final quote
    line = '46.118.127.106 - - [20/May/2015:12:05:17 +0000] "GET / HTTP/1.1" 200 235 "-" "Mozilla/5.0'
    log_line = parser.parse_line(line)
    
    assert log_line is not None
    assert log_line.user_agent == "Mozilla/5.0"
    assert log_line.response_size == 235

def test_data_parser_ipv6(parser):
    line = '2001:0db8:85a3:0000:0000:8a2e:0370:7334 - - [17/May/2015:10:05:03 +0000] "GET / HTTP/1.1" 200 123 "-" "-"'
    log_line = parser.parse_line(line)
    assert log_line is not None
    assert log_line.ip_address == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
