import pandas as pd
import pytest

from src.validator import ValidationError, validate_records


def test_validate_valid_records():
    records = [
        {
            "symbol": "TEST1",
            "ltp": 100,
        },
        {
            "symbol": "TEST2",
            "ltp": 200,
        },
    ]

    dataframe = validate_records(records, "Test Dataset")

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 2
    assert "symbol" in dataframe.columns


def test_validate_empty_records():
    with pytest.raises(ValidationError):
        validate_records([], "Test Dataset")


def test_validate_missing_symbol():
    records = [
        {
            "ltp": 100,
            "change": 5,
        }
    ]

    with pytest.raises(ValidationError):
        validate_records(records, "Test Dataset")


def test_validate_removes_duplicates():
    records = [
        {
            "symbol": "TEST1",
            "ltp": 100,
        },
        {
            "symbol": "TEST1",
            "ltp": 100,
        },
    ]

    dataframe = validate_records(records, "Test Dataset")

    assert len(dataframe) == 1