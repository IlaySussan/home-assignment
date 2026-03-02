from abc import ABC, abstractmethod
from models import LogLine

class Dimension(ABC):
    """
    An interface for representing a dimension.
    Calculates the dimension value for a given LogLine.
    """
    @abstractmethod
    def extract_data(self, log_line: LogLine) -> str:
        """Extracts the dimension string from the log line."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the dimension for reporting."""
        pass

class CountryDimension(Dimension):
    def extract_data(self, log_line: LogLine) -> str:
        return log_line.country

    @property
    def name(self) -> str:
        return "Country"

class BrowserDimension(Dimension):
    def extract_data(self, log_line: LogLine) -> str:
        return log_line.browser

    @property
    def name(self) -> str:
        return "Browser"

class OSDimension(Dimension):
    def extract_data(self, log_line: LogLine) -> str:
        return log_line.os

    @property
    def name(self) -> str:
        return "OS"
