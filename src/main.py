import argparse
import sys
from logger import get_logger
from reader import FileReader
from parser import DataParser
from enrichment import DataEnrichment
from aggregator import DataAggregator
from formatter import PercentageListFormatter
from dimensions import CountryDimension, BrowserDimension, OSDimension

logger = get_logger(__name__)


def main():
    arg_parser = argparse.ArgumentParser(description="Apache Log Statistical Reporting Module")
    arg_parser.add_argument("--log-file", type=str, required=True, help="Path to the Apache log file")
    arg_parser.add_argument("--geoip-db", type=str, required=True, help="Path to the GeoLite2-Country.mmdb file")
    args = arg_parser.parse_args()

    # 1. Initialize dimensions
    dim_country = CountryDimension()
    dim_os = OSDimension()
    dim_browser = BrowserDimension()
    dimensions = [dim_country, dim_os, dim_browser]

    # 2. Initialize Pipeline Components
    try:
        reader = FileReader(args.log_file)
    except FileNotFoundError as e:
        logger.error(f"Log file not found: {e}")
        sys.exit(1)

    try:
        enrichment = DataEnrichment(args.geoip_db)
    except Exception as e:
        logger.error(f"Error loading GeoIP database: {e}")
        sys.exit(1)

    data_parser = DataParser()
    
    # We need a separate aggregator per dimension to calculate distinct percentages
    aggregators = [DataAggregator(dim) for dim in dimensions]
    
    formatter = PercentageListFormatter()

    logger.info(f"Processing log file: {args.log_file}")
    lines_processed = 0
    lines_failed = 0

    # 3. Streaming Pipeline Execution
    for line in reader.read_lines():
        log_line = data_parser.parse_line(line)
        if not log_line:
            lines_failed += 1
            continue

        enriched_line = enrichment.enrich(log_line)
        for aggregator in aggregators:
            aggregator.add(enriched_line)
            
        lines_processed += 1

    enrichment.close()

    # 4. Format and Output Result
    logger.info(f"Finished processing. Successfully parsed: {lines_processed}, Failed: {lines_failed}\n")
    
    # Print the specific output format requested
    for aggregator in aggregators:
        print(formatter.format(aggregator.get_results(), aggregator.dimension))


if __name__ == "__main__":
    main()
