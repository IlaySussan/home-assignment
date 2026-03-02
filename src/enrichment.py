import geoip2.database
from geoip2.errors import AddressNotFoundError
from user_agents import parse as parse_user_agent
from models import LogLine

class DataEnrichment:
    """
    Enriches the data object with additional information:
    - GeoIP mapping (Country) using geoip2 database
    - User-agent parsing (Browser, OS) using user-agents library
    """
    def __init__(self, geoip_db_path: str):
        self.reader = geoip2.database.Reader(geoip_db_path)

    def enrich(self, log_line: LogLine) -> LogLine:
        """
        Takes a parsed LogLine, determines Country, Browser, and OS,
        and returns a new enriched LogLine instance.
        """
        country = "Unknown"
        browser = "Unknown"
        os_name = "Unknown"

        # Determine Country
        try:
            response = self.reader.country(log_line.ip_address)
            country = response.country.name
        except (AddressNotFoundError, ValueError):
            # Address not in database or invalid
            pass

        # Parse User Agent
        if log_line.user_agent:
            try:
                ua_info = parse_user_agent(log_line.user_agent)
                browser = ua_info.browser.family
                os_name = ua_info.os.family
            except Exception:
                pass

        # Since LogLine is frozen, we model_copy to update fields
        return log_line.model_copy(update={
            "country": country,
            "browser": browser,
            "os": os_name
        })

    def close(self):
        """Close the geoip2 reader."""
        self.reader.close()
