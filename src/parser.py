from typing import Optional
from apachelogs import LogParser, InvalidEntryError
from models import LogLine
from logger import get_logger

logger = get_logger(__name__)

# Apache Combined Log Format
COMBINED_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""


class DataParser:
    """
    Parses the log line into a LogLine data object using the apachelogs library.
    Standard Apache Combined Log Format:
    %h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-agent}i"
    """

    def __init__(self):
        self._parser = LogParser(COMBINED_LOG_FORMAT)

    def parse_line(self, line: str) -> Optional[LogLine]:
        """Parse a single Apache log line and return a LogLine model, or None on failure."""
        try:
            entry = self._parser.parse(line)
        except InvalidEntryError:
            # Fallback for truncated lines (missing ending quote for User-Agent)
            try:
                line_fallback = line.rstrip('\n\r') + '"'
                entry = self._parser.parse(line_fallback)
            except InvalidEntryError:
                logger.debug("Failed to parse line: %s", line[:80])
                return None

        # Extract request components safely
        parts = entry.request_line.split() if entry.request_line else []
        method = parts[0] if len(parts) > 0 else "-"
        url = parts[1] if len(parts) > 1 else "-"
        proto = parts[2] if len(parts) > 2 else "-"

        # response size: the library returns an int or None
        size = entry.bytes_sent if entry.bytes_sent is not None else 0

        # referer & user-agent
        referer = entry.headers_in.get("Referer")
        user_agent = entry.headers_in.get("User-Agent")

        try:
            return LogLine(
                ip_address=entry.remote_host,
                user_identifier=entry.remote_logname if entry.remote_logname != "-" else None,
                user_id=entry.remote_user if entry.remote_user else None,
                timestamp=entry.request_time.strftime("%d/%b/%Y:%H:%M:%S %z"),
                request_method=method,
                request_url=url,
                request_protocol=proto,
                status_code=entry.final_status,
                response_size=size,
                referer=referer if referer and referer != "-" else None,
                user_agent=user_agent if user_agent and user_agent != "-" else None,
            )
        except Exception as e:
            logger.error(f"Error constructing LogLine: {e}")
            return None
