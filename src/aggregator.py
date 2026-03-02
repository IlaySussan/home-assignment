from collections import Counter
from typing import List, Tuple, Dict, Any
from models import LogLine
from dimensions import Dimension

class DataAggregator:
    """
    An in-memory counter that aggregates data objects based on a given dimension.
    """
    def __init__(self, dimension: Dimension):
        self.dimension = dimension
        self.counter: Counter[str] = Counter()

    def add(self, log_line: LogLine):
        """
        Extracts keys from the log line using the dimension and increments counter.
        """
        key = self.dimension.extract_data(log_line)
        self.counter[key] += 1

    def get_results(self) -> Dict[str, int]:
        """
        Returns the raw aggregated data.
        """
        return dict(self.counter)
