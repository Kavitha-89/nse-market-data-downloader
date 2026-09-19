import argparse
import logging
import sys
from datetime import date
from typing import Callable

from src.downloader import NSEDownloadError, NSEDownloader
from src.storage import save_dataframe
from src.validator import ValidationError, validate_records


LOG_DIR = "logs"
LOG_FILE = "logs/nse_downloader.log"


def setup_logging() -> None:
    """Configure console and file logging."""

    import os

    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
    )


def process_dataset(
    dataset_name: str,
    download_function: Callable,
    output_name: str,
    downloader: NSEDownloader,
) -> bool:
    """Download, validate, and save one dataset."""

    logger = logging.getLogger(__name__)

    logger.info("Starting dataset: %s", dataset_name)

    try:
        records = download_function()

        logger.info(
            "%s: downloaded %d records.",
            dataset_name,
            len(records),
        )

        dataframe = validate_records(
            records,
            dataset_name,
        )

        output_path = save_dataframe(
            dataframe,
            output_name,
            date.today(),
        )

        logger.info(
            "%s: successfully saved %d records to %s",
            dataset_name,
            len(dataframe),
            output_path,
        )

        return True

    except (NSEDownloadError, ValidationError, ValueError) as exc:
        logger.error(
            "%s: FAILED - %s",
            dataset_name,
            exc,
        )
        return False

    except Exception:
        logger.exception(
            "%s: unexpected error.",
            dataset_name,
        )
        return False


def main() -> int:
    """Application entry point."""

    setup_logging()

    parser = argparse.ArgumentParser(
        description="Download NSE market data and save it as CSV."
    )

    parser.add_argument(
        "--dataset",
        choices=[
            "top-gainers-losers",
            "upper-band-hitters",
            "volume-gainers",
            "52-week-high",
        ],
        help="Download only the selected dataset.",
    )

    args = parser.parse_args()

    downloader = NSEDownloader()

    datasets = {
        "top-gainers-losers": [
            (
                "Top Gainers",
                downloader.download_top_gainers,
                "top-gainers",
            ),
            (
                "Top Losers",
                downloader.download_top_losers,
                "top-losers",
            ),
        ],
        "upper-band-hitters": [
            (
                "Upper Band Hitters",
                downloader.download_upper_band,
                "upper-band-hitters",
            ),
        ],
        "volume-gainers": [
            (
                "Volume Gainers",
                downloader.download_volume_gainers,
                "volume-gainers",
            ),
        ],
        "52-week-high": [
            (
                "52 Week High",
                downloader.download_52_week_high,
                "52-week-high",
            ),
        ],
    }

    selected_datasets = (
        datasets.values()
        if args.dataset is None
        else [datasets[args.dataset]]
    )

    results = []

    for dataset_group in selected_datasets:
        for dataset_name, function, output_name in dataset_group:
            success = process_dataset(
                dataset_name,
                function,
                output_name,
                downloader,
            )
            results.append(success)

    if all(results):
        logging.info("All selected datasets completed successfully.")
        return 0

    logging.error(
        "One or more datasets failed. "
        "Successful datasets were still processed."
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())