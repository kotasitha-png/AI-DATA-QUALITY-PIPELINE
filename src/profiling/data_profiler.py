from typing import Any, Dict, List

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import NumericType


def profile_dataframe(df: DataFrame) -> Dict[str, Any]:
    """
    Generate a generic profile for a Spark DataFrame.

    Returns dataset-level metrics and column-level statistics.
    """

    total_rows = df.count()
    total_columns = len(df.columns)

    profile = {
        "row_count": total_rows,
        "column_count": total_columns,
        "columns": [],
    }

    for field in df.schema.fields:

        column_name = field.name
        data_type = field.dataType

        column_profile = profile_column(
            df=df,
            column_name=column_name,
            total_rows=total_rows,
            is_numeric=isinstance(
                data_type,
                NumericType,
            ),
            data_type=data_type.simpleString(),
        )

        profile["columns"].append(
            column_profile
        )

    return profile


def profile_column(
    df: DataFrame,
    column_name: str,
    total_rows: int,
    is_numeric: bool,
    data_type: str,
) -> Dict[str, Any]:
    """
    Profile a single DataFrame column.
    """

    null_count = (
        df
        .filter(
            F.col(column_name).isNull()
        )
        .count()
    )

    distinct_count = (
        df
        .select(column_name)
        .distinct()
        .count()
    )

    if total_rows > 0:

        null_percentage = (
            null_count
            / total_rows
            * 100
        )

        distinct_percentage = (
            distinct_count
            / total_rows
            * 100
        )

    else:

        null_percentage = 0.0
        distinct_percentage = 0.0

    column_profile = {
        "name": column_name,
        "data_type": data_type,
        "null_count": null_count,
        "null_percentage": round(
            null_percentage,
            2,
        ),
        "distinct_count": distinct_count,
        "distinct_percentage": round(
            distinct_percentage,
            2,
        ),
    }

    if is_numeric:

        numeric_stats = (
            df
            .select(
                F.min(column_name)
                .alias("min"),

                F.max(column_name)
                .alias("max"),

                F.avg(column_name)
                .alias("mean"),
            )
            .first()
        )

        column_profile["min"] = (
            numeric_stats["min"]
        )

        column_profile["max"] = (
            numeric_stats["max"]
        )

        column_profile["mean"] = (
            round(
                numeric_stats["mean"],
                2,
            )
            if numeric_stats["mean"]
            is not None
            else None
        )

    return column_profile