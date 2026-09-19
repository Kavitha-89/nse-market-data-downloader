from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

NSE_BASE_URL = "https://www.nseindia.com"

DATASETS = {
    "top-gainers-losers": {
        "name": "Top Gainers and Losers",
        "endpoints": {
            "gainers": (
                f"{NSE_BASE_URL}/api/live-analysis-variations"
                "?index=gainers"
            ),
            "losers": (
                f"{NSE_BASE_URL}/api/live-analysis-variations"
                "?index=loosers"
            ),
        },
    },
    "upper-band-hitters": {
        "name": "Upper Band Hitters",
        "url": (
            f"{NSE_BASE_URL}/api/live-analysis-price-band-hitter"
        ),
    },
    "volume-gainers": {
        "name": "Volume Gainers",
        "url": (
            f"{NSE_BASE_URL}/api/live-analysis-volume-gainers"
        ),
    },
    "52-week-high": {
        "name": "52 Week High",
        "url": (
            f"{NSE_BASE_URL}/api/live-analysis-data-52weekhighstock"
        ),
    },
}


REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


NSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}