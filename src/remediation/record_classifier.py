from typing import Any, Dict, Tuple

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.quality.conditions import (
    build_failure_condition,
)


def classify_records(
    df: DataFrame,
    config: Dict[str, Any],
) -> DataFrame:
    """
    Evaluate row-level quality rules and add
    quality metadata to every record.
    """

    available_columns = set(df.columns)

    failed_rule_expressions = []

    for rule in config["rules"]:

        column = rule["column"]

        if column not in available_columns:
            raise ValueError(
                f"Rule {rule['rule_id']} "
                f"references missing column: "
                f"{column}"
            )

        failure_condition = (
            build_failure_condition(
                df,
                rule,
            )
        )

        failed_rule_expressions.append(
            F.when(
                failure_condition,
                F.lit(rule["rule_id"]),
            )
        )

    failed_rules_array = F.filter(
        F.array(
            *failed_rule_expressions
        ),
        lambda item: item.isNotNull(),
    )

    classified_df = (
        df
        .withColumn(
            "_dq_failed_rules",
            failed_rules_array,
        )
        .withColumn(
            "_dq_failure_count",
            F.size(
                F.col("_dq_failed_rules")
            ),
        )
        .withColumn(
            "_dq_status",
            F.when(
                F.col(
                    "_dq_failure_count"
                ) == 0,
                F.lit("VALID"),
            ).otherwise(
                F.lit("FAILED")
            ),
        )
        .withColumn(
    "_dq_processed_at",
    F.current_timestamp(),
        )
    )

    return classified_df


def split_valid_quarantine(
    classified_df: DataFrame,
) -> Tuple[DataFrame, DataFrame]:
    """
    Split classified records into valid
    and quarantined DataFrames.
    """

    valid_df = (
        classified_df
        .filter(
            F.col("_dq_status")
            == "VALID"
        )
    )

    quarantine_df = (
        classified_df
        .filter(
            F.col("_dq_status")
            == "FAILED"
        )
    )

    return (
        valid_df,
        quarantine_df,
    )