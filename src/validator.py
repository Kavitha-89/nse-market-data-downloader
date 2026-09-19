import logging
from typing import Any

import pandas as pd


logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when downloaded NSE data fails validation."""


def validate_records(
    records: list[dict[str, Any]],
    dataset_name: str,
) -> pd.DataFrame:
    """
    Validate downloaded NSE records and return a DataFrame.

    Checks:
    - response contains records
    - records are dictionaries
    - records contain useful columns
    - symbol column exists when expected
    - duplicate records are detected
    """

    if not records:
        raise ValidationError(
            f"{dataset_name}: response contains no records."
        )

    if not all(isinstance(record, dict) for record in records):
        raise ValidationError(
            f"{dataset_name}: response contains invalid records."
        )

    dataframe = pd.DataFrame(records)

    if dataframe.empty:
        raise ValidationError(
            f"{dataset_name}: DataFrame is empty."
        )

    if len(dataframe.columns) == 0:
        raise ValidationError(
            f"{dataset_name}: no columns were returned."
        )

    # Most NSE datasets contain a symbol identifying the security.
    if "symbol" not in dataframe.columns:
        raise ValidationError(
            f"{dataset_name}: required 'symbol' column is missing."
        )

    # A security symbol should not be empty.
    if dataframe["symbol"].isna().all():
        raise ValidationError(
            f"{dataset_name}: all symbol values are empty."
        )

    duplicate_count = int(dataframe.duplicated().sum())

    if duplicate_count > 0:
        logger.warning(
            "%s: found %d duplicate records.",
            dataset_name,
            duplicate_count,
        )

        dataframe = dataframe.drop_duplicates().reset_index(drop=True)

    if dataframe.empty:
        raise ValidationError(
            f"{dataset_name}: no records remain after validation."
        )

    logger.info(
        "%s: validation successful. %d records, %d columns.",
        dataset_name,
        len(dataframe),
        len(dataframe.columns),
    )

    return dataframe