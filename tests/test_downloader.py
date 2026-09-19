import pytest

from src.downloader import NSEDownloadError, NSEDownloader


class FakeResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
        self.content = b"test"

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._data


def test_download_top_gainers(monkeypatch):
    downloader = NSEDownloader()

    fake_data = {
        "allSec": {
            "data": [
                {"symbol": "TEST1", "ltp": 100},
                {"symbol": "TEST2", "ltp": 200},
            ]
        }
    }

    monkeypatch.setattr(
        downloader.session,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data),
    )

    records = downloader.download_top_gainers()

    assert len(records) == 2
    assert records[0]["symbol"] == "TEST1"


def test_download_top_losers(monkeypatch):
    downloader = NSEDownloader()

    fake_data = {
        "allSec": {
            "data": [
                {"symbol": "TEST1", "ltp": 90},
            ]
        }
    }

    monkeypatch.setattr(
        downloader.session,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data),
    )

    records = downloader.download_top_losers()

    assert len(records) == 1
    assert records[0]["symbol"] == "TEST1"


def test_download_upper_band(monkeypatch):
    downloader = NSEDownloader()

    fake_data = {
        "upper": {
            "AllSec": {
                "data": [
                    {"symbol": "TEST1", "ltp": 100},
                ]
            }
        }
    }

    monkeypatch.setattr(
        downloader.session,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data),
    )

    records = downloader.download_upper_band()

    assert len(records) == 1
    assert records[0]["symbol"] == "TEST1"


def test_download_volume_gainers(monkeypatch):
    downloader = NSEDownloader()

    fake_data = {
        "data": [
            {"symbol": "TEST1", "ltp": 150},
        ]
    }

    monkeypatch.setattr(
        downloader.session,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data),
    )

    records = downloader.download_volume_gainers()

    assert len(records) == 1
    assert records[0]["symbol"] == "TEST1"


def test_download_52_week_high(monkeypatch):
    downloader = NSEDownloader()

    fake_data = {
        "data": [
            {"symbol": "TEST1", "ltp": 250},
        ]
    }

    monkeypatch.setattr(
        downloader.session,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data),
    )

    records = downloader.download_52_week_high()

    assert len(records) == 1
    assert records[0]["symbol"] == "TEST1"


def test_download_rejects_invalid_json(monkeypatch):
    downloader = NSEDownloader()

    class InvalidJsonResponse:
        status_code = 200
        content = b"invalid"

        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Invalid JSON")

    monkeypatch.setattr(
        downloader.session,
        "get",
        lambda *args, **kwargs: InvalidJsonResponse(),
    )

    with pytest.raises(NSEDownloadError):
        downloader.download_volume_gainers()