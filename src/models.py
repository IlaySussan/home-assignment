from pydantic import BaseModel, Field
from typing import Optional

class LogLine(BaseModel):
    """
    Represents a parsed and potentially enriched Apache log line.
    Frozen is True so it can be hashable and used in Sets or Counters if needed.
    """
    ip_address: str
    user_identifier: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: str
    request_method: str
    request_url: str
    request_protocol: str
    status_code: int
    response_size: int = 0
    referer: Optional[str] = None
    user_agent: Optional[str] = None

    # Enriched Fields
    country: str = "Unknown"
    browser: str = "Unknown"
    os: str = "Unknown"

    model_config = {
        "frozen": True
    }
