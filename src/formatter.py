from abc import ABC, abstractmethod
from typing import Dict
from dimensions import Dimension

class ResultFormatter(ABC):
    """
    An interface that decides how the result will be formatted.
    """
    @abstractmethod
    def format(self, aggregated_data: Dict[str, int], dimension: Dimension) -> str:
        """Format the aggregated data for a single dimension."""
        pass

class PercentageListFormatter(ResultFormatter):
    """
    Formats the aggregated data into a list of percentages sorted descending,
    matching the assignment's required format.
    """
    def format(self, aggregated_data: Dict[str, int], dimension: Dimension) -> str:
        if not aggregated_data:
            return f"{dimension.name}:\nNo data\n"

        total_count = sum(aggregated_data.values())
        if total_count == 0:
            return f"{dimension.name}:\nNo data\n"
            
        # Separate out existing "Other" if the parsing library returned it naturally
        other_key = "Other"
        native_other_count = aggregated_data.pop(other_key, 0)
        
        # Sort remaining keys by count descending
        sorted_keys = sorted(aggregated_data.keys(), key=lambda k: aggregated_data[k], reverse=True)
        
        # Take the top 5
        top_keys = sorted_keys[:5]
        
        # Sum the rest natively plus the existing "Other" count
        other_count = native_other_count
        for key in sorted_keys[5:]:
            other_count += aggregated_data[key]
            
        lines = [f"{dimension.name}:"]
        
        # Add top 5 to output
        for key in top_keys:
            count = aggregated_data[key]
            percentage = (count / total_count) * 100
            lines.append(f"{key} {percentage:.2f}%")
            
        # Add "Other" to output if it has a count > 0
        if other_count > 0:
            percentage = (other_count / total_count) * 100
            lines.append(f"{other_key} {percentage:.2f}%")
            
        return "\n".join(lines) + "\n"
