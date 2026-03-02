# Home Assignment - Statistical Reporting Module

A robust, memory-efficient Python 3.13 pipeline that parses Apache web server logs, enriches them with GeoIP and User-Agent data, and outputs statistical aggregations.

## Prerequisites
- **Python 3.13**
- [**uv**](https://docs.astral.sh/uv/) (Python package dependency manager)
- **GeoLite2-Country.mmdb** (MaxMind GeoIP2 Database placed in the root directory)
- **apache_log.txt** (Apache Combined Log Format file placed in the root directory)

## Setup

1. **Install dependencies and setup Virtual Environment:**
   Run `uv` to automatically create a virtual environment (`.venv`) and install all required dependencies:
   ```bash
   uv sync
   ```

## Running the Application

This project uses a streaming pipeline to process the log file line-by-line, parsing it using the `apachelogs` library and grouping records by Country, OS, and Browser.

You can run the script via `uv run` while explicitly pointing `PYTHONPATH` to the `src` directory:

#### On Windows (PowerShell):
```powershell
$env:PYTHONPATH="src"
uv run python src/main.py --log-file apache_log.txt --geoip-db GeoLite2-Country.mmdb
```

#### On Linux / macOS (Bash):
```bash
PYTHONPATH=src uv run python src/main.py --log-file apache_log.txt --geoip-db GeoLite2-Country.mmdb
```

## Running Tests

Tests are written using `pytest`. You can run the test suite to verify the parser implementation:

#### On Windows (PowerShell):
```powershell
$env:PYTHONPATH="src"
uv run pytest -v
```

#### On Linux / macOS (Bash):
```bash
PYTHONPATH=src uv run pytest -v
```

## Architecture Notes
- The application processes the log line-by-line avoiding out-of-memory errors on large log files.
- Extensible `Dimension` classes allow easy additions of new grouping criteria without modifying the aggregator logic.
- Graceful error handling defaults unknown IP addresses or User-Agents to "Unknown" rather than crashing or skipping the dimensions.