from datetime import date

import pandas as pd
import pytest

import src.storage as storage


def test_save_dataframe_creates_csv(tmp_path, monkeypatch):
    dataframe = pd.DataFrame(
        [
            {"symbol": "TEST1", "ltp": 100},
            {"symbol": "TEST2", "ltp": 200},
        ]
    )

    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    output_path = storage.save_dataframe(
        dataframe,
        "Test Dataset",
        date(2026, 9, 19),
    )

    assert output_path.exists()
    assert output_path.name == "test-dataset_2026-09-19.csv"

    saved_dataframe = pd.read_csv(output_path)

    assert len(saved_dataframe) == 2
    assert list(saved_dataframe["symbol"]) == ["TEST1", "TEST2"]


def test_save_dataframe_rejects_empty_dataframe(tmp_path, monkeypatch):
    dataframe = pd.DataFrame()

    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    with pytest.raises(ValueError):
        storage.save_dataframe(
            dataframe,
            "Test Dataset",
            date(2026, 9, 19),
        )


def test_save_dataframe_overwrites_same_day_file(tmp_path, monkeypatch):
    first_dataframe = pd.DataFrame(
        [{"symbol": "TEST1", "ltp": 100}]
    )

    second_dataframe = pd.DataFrame(
        [
            {"symbol": "TEST1", "ltp": 100},
            {"symbol": "TEST2", "ltp": 200},
        ]
    )

    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    first_path = storage.save_dataframe(
        first_dataframe,
        "Test Dataset",
        date(2026, 9, 19),
    )

    second_path = storage.save_dataframe(
        second_dataframe,
        "Test Dataset",
        date(2026, 9, 19),
    )

    assert first_path == second_path

    saved_dataframe = pd.read_csv(second_path)

    assert len(saved_dataframe) == 2