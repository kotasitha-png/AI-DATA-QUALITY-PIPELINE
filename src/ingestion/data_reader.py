from pathlib import Path
from typing import Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType


SUPPORTED_FORMATS = {
    "csv",
    "json",
    "parquet",
}


def read_dataset(
    spark: SparkSession,
    path: str,
    file_format: str,
    schema: Optional[StructType] = None,
    header: bool = True,
    infer_schema: bool = True,
) -> DataFrame:
    """
    Read a dataset into a Spark DataFrame.

    Supported formats:
    - CSV
    - JSON
    - Parquet

    Parameters
    ----------
    spark:
        Active SparkSession.

    path:
        Input file or directory.

    file_format:
        csv, json, or parquet.

    schema:
        Optional explicit Spark schema.

    header:
        Whether CSV contains a header.

    infer_schema:
        Whether Spark should infer column datatypes
        when an explicit schema is not provided.
    """

    normalized_format = file_format.lower()

    if normalized_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format: {file_format}. "
            f"Supported formats: "
            f"{sorted(SUPPORTED_FORMATS)}"
        )

    validate_path(path)

    if normalized_format == "csv":

        reader = (
            spark.read
            .option("header", str(header).lower())
            .option(
                "inferSchema",
                str(
                    infer_schema
                    and schema is None
                ).lower(),
            )
        )

        if schema is not None:
            reader = reader.schema(schema)

        return reader.csv(path)

    if normalized_format == "json":

        reader = spark.read

        if schema is not None:
            reader = reader.schema(schema)

        return reader.json(path)

    if normalized_format == "parquet":

        return spark.read.parquet(path)

    raise RuntimeError(
        "Dataset reader reached an unexpected state."
    )


def validate_path(path: str) -> None:
    """
    Validate that a local input path exists.

    This check is intended for local development.
    Cloud/distributed paths will be handled differently later.
    """

    input_path = Path(path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {path}"
        )