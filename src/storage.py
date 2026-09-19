from datetime import date
from pathlib import Path

import pandas as pd

from config import DATA_DIR


def save_dataframe(
    dataframe: pd.DataFrame,
    dataset_name: str,
    trading_date: date | None = None,
) -> Path:
    """
    Save a validated DataFrame as a dated CSV file.

    The filename is deterministic for a given dataset and date,
    so repeated runs on the same day do not create duplicate files.
    """

    if dataframe.empty:
        raise ValueError(
            f"Cannot save empty dataset: {dataset_name}"
        )

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if trading_date is None:
        trading_date = date.today()

    safe_name = (
        dataset_name.lower()
        .replace(" ", "-")
        .replace("/", "-")
    )

    filename = f"{safe_name}_{trading_date.isoformat()}.csv"
    output_path = DATA_DIR / filename

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    return output_path