from pathlib import Path
from typing import Tuple

from pyspark.sql import DataFrame


def write_quality_outputs(
    valid_df: DataFrame,
    quarantine_df: DataFrame,
    valid_path: str,
    quarantine_path: str,
    mode: str = "overwrite",
) -> Tuple[str, str]:
    """
    Persist valid and quarantined records
    as Parquet datasets.
    """

    Path(valid_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(quarantine_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    (
        valid_df
        .write
        .mode(mode)
        .parquet(valid_path)
    )

    (
        quarantine_df
        .write
        .mode(mode)
        .parquet(
            quarantine_path
        )
    )

    return (
        valid_path,
        quarantine_path,
    )