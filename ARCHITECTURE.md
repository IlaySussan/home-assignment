# Statistical Reporting Module - Design

## 1. High-level architecture and component breakdown:
    this module processes the Apache web server log file line-by-line to ensure memory efficiency and prevent memory leak.

    The pipline consists of five components:
    1. File Reader -  reads the given Apache web server log file line by line.
    2. Data Parser - parses the log line into a data object ( pydantic BaseModel).
    3. Data Enrichment - enriches the data object with additional information( using the geoip2 database and the user-agent parser).
    4. Data Aggregator - an in memory counter that aggregates the data object into a single object ( using the data object as a key).
    5. Result Formatter - formats the aggregated data object into a string.


## 2. Key abstractions and interfaces:
    * LogLine - a pydantic model that represents a log line.
    * Dimension - an interface for representing a dimension which contains one method whihc must be implemented - extract_data(log_line:LogLine).
    * ResultFormatter - an interface that decides how the result will be formatted.

## 3. Extensibility:
    * adding new dimension - we can simply need to create a new class the inherits from Dimension and implement the extract_data method.
    * adding new result formatter - we can simply need to create a new class the inherits from ResultFormatter and implement the format method.
    * changing the file reader - we can easily replace the file reader with a different data source reader (for example).

## 4. Technology choices and rationale:
    * language - python 3.13 - it is a modern language that is easy to learn and use, and it has a large community and a lot of libraries that can help us build the application (for example - the user-agents library).
    * uv - for a very fast dependency resolution and virtual environment management.
    * pydantic - for data validation and data modeling.
    * geoip2 - for ip geolocation.
    * user-agents - for user-agent parsing.

## 5. Trade-offs and assumptions:
    * in-memroy management vs external database - for simplicity and performance, we chose to use in-memory management. This is a trade-off because it means that the application will not be able to handle very large log files and if our application crashes the aggregated data will be lost. but in this case where we only need to parse a 10,000 line log file this way we will be able to avoid the overhead and latency of using an external database.

    * error-handlng - we assume that the log file is valid and that the geoip2 database and the user-agent parser will work as expected. if we will receive a request from an unrecognized country or an invalid line containing an invalid os or browser we eill simply place a default value of "Unknown" for the relevant field.