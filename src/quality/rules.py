from typing import Any, Dict

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.quality.models import RuleResult


def evaluate_not_null(
    df: DataFrame,
    rule: Dict[str, Any],
) -> RuleResult:

    column = rule["column"]
    total_count = df.count()

    failed_count = (
        df
        .filter(
            F.col(column).isNull()
        )
        .count()
    )

    return build_result(
        rule=rule,
        failed_count=failed_count,
        total_count=total_count,
        condition_description=(
            f"{column} must not be null"
        ),
    )


def evaluate_unique(
    df: DataFrame,
    rule: Dict[str, Any],
) -> RuleResult:

    column = rule["column"]
    total_count = df.count()

    duplicate_values = (
        df
        .groupBy(column)
        .count()
        .filter(
            F.col("count") > 1
        )
    )

    failed_count_row = (
        duplicate_values
        .select(
            F.sum(
                F.col("count") - 1
            ).alias("duplicate_count")
        )
        .first()
    )

    failed_count = (
        failed_count_row[
            "duplicate_count"
        ]
        or 0
    )

    return build_result(
        rule=rule,
        failed_count=int(
            failed_count
        ),
        total_count=total_count,
        condition_description=(
            f"{column} must be unique"
        ),
    )


def evaluate_range(
    df: DataFrame,
    rule: Dict[str, Any],
) -> RuleResult:

    column = rule["column"]

    minimum = rule.get("min")
    maximum = rule.get("max")

    total_count = df.count()

    condition = None

    if minimum is not None:

        condition = (
            F.col(column) < minimum
        )

    if maximum is not None:

        max_condition = (
            F.col(column) > maximum
        )

        condition = (
            max_condition
            if condition is None
            else condition
            | max_condition
        )

    if condition is None:

        raise ValueError(
            "Range rule requires min "
            "and/or max."
        )

    failed_count = (
        df
        .filter(condition)
        .count()
    )

    description = (
        f"{column} range:"
        f" min={minimum},"
        f" max={maximum}"
    )

    return build_result(
        rule=rule,
        failed_count=failed_count,
        total_count=total_count,
        condition_description=description,
    )


def evaluate_regex(
    df: DataFrame,
    rule: Dict[str, Any],
) -> RuleResult:

    column = rule["column"]
    pattern = rule["pattern"]

    total_count = df.count()

    failed_count = (
        df
        .filter(
            F.col(column).isNotNull()
            &
            ~F.col(column).rlike(
                pattern
            )
        )
        .count()
    )

    return build_result(
        rule=rule,
        failed_count=failed_count,
        total_count=total_count,
        condition_description=(
            f"{column} must match regex"
        ),
    )


def evaluate_allowed_values(
    df: DataFrame,
    rule: Dict[str, Any],
) -> RuleResult:

    column = rule["column"]
    values = rule["values"]

    total_count = df.count()

    failed_count = (
        df
        .filter(
            F.col(column).isNotNull()
            &
            ~F.col(column).isin(values)
        )
        .count()
    )

    return build_result(
        rule=rule,
        failed_count=failed_count,
        total_count=total_count,
        condition_description=(
            f"{column} must contain "
            f"an allowed value"
        ),
    )


def build_result(
    rule: Dict[str, Any],
    failed_count: int,
    total_count: int,
    condition_description: str,
) -> RuleResult:

    if total_count > 0:

        failure_percentage = (
            failed_count
            / total_count
            * 100
        )

    else:

        failure_percentage = 0.0

    passed = (
        failed_count == 0
    )

    if passed:

        message = (
            f"{rule['rule_id']} passed."
        )

    else:

        message = (
            f"{rule['rule_id']} failed "
            f"for {failed_count:,} rows."
        )

    return RuleResult(
        rule_id=rule["rule_id"],
        rule_type=rule["type"],
        column=rule["column"],
        severity=rule.get(
            "severity",
            "medium",
        ),
        passed=passed,
        failed_count=failed_count,
        total_count=total_count,
        failure_percentage=round(
            failure_percentage,
            2,
        ),
        message=message,
        condition_description=(
            condition_description
        ),
    )