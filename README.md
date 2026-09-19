# NSE Market Data Downloader

A Python command-line application that downloads NSE market data from official NSE API endpoints, validates the responses, and saves the results as dated CSV files.

## Features

- Downloads all required NSE market-data datasets.
- Supports:
  - Top Gainers
  - Top Losers
  - Upper Band Hitters
  - Volume Gainers
  - 52 Week High
- Saves data automatically as CSV files.
- Uses dated filenames to avoid confusing duplicate files.
- Supports downloading all datasets or selecting an individual dataset.
- Includes request timeout and retry handling.
- Handles HTTP errors, invalid JSON, empty responses, and unexpected response structures.
- Validates downloaded records before saving.
- Removes duplicate records during validation.
- Logs download attempts, failures, validation results, and saved record counts.
- A failure in one dataset does not prevent the remaining datasets from being processed.
- Includes automated unit tests.

## Project Structure

```text
nse-market-data-downloader/
│
├── config.py
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   └── *.csv
│
├── logs/
│   └── nse_downloader.log
│
├── src/
│   ├── __init__.py
│   ├── downloader.py
│   ├── storage.py
│   └── validator.py
│
└── tests/
    ├── test_downloader.py
    ├── test_storage.py
    └── test_validator.py

## Requirements

Requirements
Python 3.13+
requests
pandas
pytest

## Install the dependencies with:

pip install -r requirements.txt
Running the Application

To download all datasets:

python main.py

To download only one dataset:

python main.py --dataset top-gainers-losers

## Available dataset options:

top-gainers-losers
upper-band-hitters
volume-gainers
52-week-high
Data Acquisition

The application communicates with NSE API endpoints rather than manually copying data from web pages.

## The four assignment pages are:

Top Gainers / Losers
Upper Band Hitters
Volume Gainers / Spurts
52 Week High - Equity Market

The Top Gainers / Losers page contains two datasets, so the application downloads and stores Top Gainers and Top Losers separately.

The NSE API endpoints and configuration are kept in config.py, while the acquisition logic is implemented in src/downloader.py.

## Validation

Downloaded data is validated before it is written to disk.

The validation process checks:

The response contains records.
Records are dictionaries.
The resulting DataFrame is not empty.
At least one column is present.
A symbol column exists.
Symbol values are not all empty.
Duplicate records are detected and removed.

Invalid or unexpected responses are rejected instead of being saved as CSV files.

## Storage

CSV files are stored in the data/ directory.

Example filenames:

top-gainers_2026-09-19.csv
top-losers_2026-09-19.csv
upper-band-hitters_2026-09-19.csv
volume-gainers_2026-09-19.csv
52-week-high_2026-09-19.csv

The filename includes the trading date.

If the same dataset is downloaded again on the same day, the existing dated file is overwritten rather than creating multiple confusing copies.

## Error Handling

The downloader includes:

Request timeout handling
HTTP error handling
Invalid JSON handling
Empty response handling
Unexpected JSON structure handling
Retry attempts with backoff

Each request can be attempted up to three times.

If a dataset fails, the error is logged and processing continues with the remaining datasets.

## Logging

Execution logs are written to:

logs/nse_downloader.log

The logs include information such as:

Dataset being processed
Request attempts
Request success or failure
Retry attempts
Validation results
Record counts
Output file paths
Errors and exceptions
Testing

The project includes automated tests for:

NSE response extraction
Invalid JSON handling
Data validation
Empty datasets
Missing required columns
Duplicate records
CSV file creation
Empty-data rejection
Same-day file handling

## Run the complete test suite with:

python -m pytest -v

Expected result:

13 passed
Sample Output

The application has been tested against the NSE endpoints and successfully downloaded sample datasets.

Example record counts from a successful run:

Top Gainers: 20
Top Losers: 20
Upper Band Hitters: 152
Volume Gainers: 25
52 Week High: 113

These values represent a sample execution and may change depending on the NSE market data available at the time of execution.

## Design

The project separates responsibilities into different modules:

config.py — URLs, headers, retry and timeout configuration
src/downloader.py — NSE API acquisition and request handling
src/validator.py — data validation and duplicate handling
src/storage.py — CSV file storage
main.py — command-line entry point and orchestration
tests/ — automated tests

This structure keeps acquisition, validation, storage, and application entry-point responsibilities separate and makes the downloader easier to extend.

## Limitations
The application depends on NSE API availability and response formats.
NSE API response structures may change in the future.
The application currently stores CSV files locally.
No database or notification system is included because they are outside the core assignment requirements.
The Top Gainers / Losers page is represented by two CSV files because it contains two separate datasets.