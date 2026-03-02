import os
from typing import Generator

class FileReader:
    """
    Reads the given file line by line to ensure memory efficiency.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Log file not found: {self.file_path}")

    def read_lines(self) -> Generator[str, None, None]:
        """
        Yields lines from the file one by one.
        """
        with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    yield stripped
