\# NSE Market Data Downloader



A Python application that automatically downloads selected NSE market-data datasets and stores the results as dated CSV files.



\## Objective



This project retrieves market data from NSE endpoints corresponding to:



1\. Top Gainers / Losers

2\. Upper Band Hitters

3\. Volume Gainers / Spurts

4\. 52 Week High - Equity Market



The application is designed as a small production-minded data pipeline with separate acquisition, validation, storage, and entry-point layers.



\## Features



\- Downloads all required NSE market-data datasets.

\- Supports downloading an individual dataset using the command line.

\- Uses HTTP timeouts and retry logic.

\- Handles HTTP failures, invalid JSON, empty responses, and unexpected response structures.

\- Validates downloaded records before saving.

\- Detects and removes duplicate records.

\- Saves data as CSV files with deterministic trading-date filenames.

\- Re-running a dataset on the same day overwrites the existing dated file instead of creating confusing duplicate files.

\- Logs download attempts, failures, validation results, record counts, and saved file paths.

\- A failure in one dataset does not prevent other selected datasets from being processed.

\- Includes automated unit tests using pytest.



\## Project Structure



```text

nse-market-data-downloader/

│

├── config.py

├── main.py

├── README.md

├── requirements.txt

│

├── data/

│   └── Generated CSV files

│

├── logs/

│   └── nse\_downloader.log

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── downloader.py

│   ├── storage.py

│   └── validator.py

│

└── tests/

&#x20;   ├── test\_downloader.py

&#x20;   ├── test\_storage.py

&#x20;   └── test\_validator.py

