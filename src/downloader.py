import logging
import time
from typing import Any

import requests

from config import (
    DATASETS,
    MAX_RETRIES,
    NSE_HEADERS,
    REQUEST_TIMEOUT,
    RETRY_BACKOFF_SECONDS,
)


logger = logging.getLogger(__name__)


class NSEDownloadError(Exception):
    """Raised when an NSE dataset cannot be downloaded or parsed."""


class NSEDownloader:
    """Downloads JSON market data from NSE APIs."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(NSE_HEADERS)

    def _request_json(self, url: str) -> dict[str, Any]:
        """Request JSON from NSE with retries and error handling."""

        last_error: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(
                    "Request attempt %d/%d: %s",
                    attempt,
                    MAX_RETRIES,
                    url,
                )

                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT,
                )

                response.raise_for_status()

                if not response.content:
                    raise NSEDownloadError(
                        "NSE returned an empty response."
                    )

                try:
                    data = response.json()
                except ValueError as exc:
                    raise NSEDownloadError(
                        "NSE returned invalid JSON."
                    ) from exc

                if not isinstance(data, dict):
                    raise NSEDownloadError(
                        "NSE response is not a JSON object."
                    )

                logger.info(
                    "Request successful: HTTP %s",
                    response.status_code,
                )

                return data

            except (requests.RequestException, NSEDownloadError) as exc:
                last_error = exc

                logger.warning(
                    "Request failed on attempt %d/%d: %s",
                    attempt,
                    MAX_RETRIES,
                    exc,
                )

                if attempt < MAX_RETRIES:
                    sleep_time = RETRY_BACKOFF_SECONDS * attempt
                    logger.info(
                        "Retrying in %d seconds...",
                        sleep_time,
                    )
                    time.sleep(sleep_time)

        raise NSEDownloadError(
            f"Failed to download NSE data after "
            f"{MAX_RETRIES} attempts: {last_error}"
        )

    def download_top_gainers(self) -> list[dict[str, Any]]:
        """Download Top Gainers data."""

        url = DATASETS["top-gainers-losers"]["endpoints"]["gainers"]
        response = self._request_json(url)

        try:
            records = response["allSec"]["data"]
        except (KeyError, TypeError) as exc:
            raise NSEDownloadError(
                "Unexpected Top Gainers response structure."
            ) from exc

        if not isinstance(records, list):
            raise NSEDownloadError(
                "Top Gainers data is not a list."
            )

        return records

    def download_top_losers(self) -> list[dict[str, Any]]:
        """Download Top Losers data."""

        url = DATASETS["top-gainers-losers"]["endpoints"]["losers"]
        response = self._request_json(url)

        try:
            records = response["allSec"]["data"]
        except (KeyError, TypeError) as exc:
            raise NSEDownloadError(
                "Unexpected Top Losers response structure."
            ) from exc

        if not isinstance(records, list):
            raise NSEDownloadError(
                "Top Losers data is not a list."
            )

        return records

    def download_upper_band(self) -> list[dict[str, Any]]:
        """Download Upper Band Hitters data."""

        url = DATASETS["upper-band-hitters"]["url"]
        response = self._request_json(url)

        try:
            records = response["upper"]["AllSec"]["data"]
        except (KeyError, TypeError) as exc:
            raise NSEDownloadError(
                "Unexpected Upper Band response structure."
            ) from exc

        if not isinstance(records, list):
            raise NSEDownloadError(
                "Upper Band data is not a list."
            )

        return records

    def download_volume_gainers(self) -> list[dict[str, Any]]:
        """Download Volume Gainers data."""

        url = DATASETS["volume-gainers"]["url"]
        response = self._request_json(url)

        try:
            records = response["data"]
        except (KeyError, TypeError) as exc:
            raise NSEDownloadError(
                "Unexpected Volume Gainers response structure."
            ) from exc

        if not isinstance(records, list):
            raise NSEDownloadError(
                "Volume Gainers data is not a list."
            )

        return records

    def download_52_week_high(self) -> list[dict[str, Any]]:
        """Download 52 Week High data."""

        url = DATASETS["52-week-high"]["url"]
        response = self._request_json(url)

        try:
            records = response["data"]
        except (KeyError, TypeError) as exc:
            raise NSEDownloadError(
                "Unexpected 52 Week High response structure."
            ) from exc

        if not isinstance(records, list):
            raise NSEDownloadError(
                "52 Week High data is not a list."
            )

        return records