from typing import Any, Dict

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def build_failure_condition(
    df: DataFrame,
    rule: Dict[str, Any],
) -> Column:
    """
    Build a Spark Boolean expression representing
    when a row fails a configured data-quality rule.
    """

    rule_type = rule["type"].lower()
    column = rule["column"]

    if rule_type == "not_null":

        return F.col(column).isNull()

    if rule_type == "range":

        minimum = rule.get("min")
        maximum = rule.get("max")

        condition = None

        if minimum is not None:
            condition = (
                F.col(column).isNotNull()
                &
                (F.col(column) < minimum)
            )

        if maximum is not None:

            max_condition = (
                F.col(column).isNotNull()
                &
                (F.col(column) > maximum)
            )

            condition = (
                max_condition
                if condition is None
                else condition | max_condition
            )

        if condition is None:
            raise ValueError(
                f"Range rule {rule['rule_id']} "
                "must define min and/or max."
            )

        return condition

    if rule_type == "regex":

        pattern = rule["pattern"]

        return (
            F.col(column).isNotNull()
            &
            ~F.col(column).rlike(pattern)
        )

    if rule_type == "allowed_values":

        values = rule["values"]

        return (
            F.col(column).isNotNull()
            &
            ~F.col(column).isin(values)
        )

    if rule_type == "unique":

        duplicate_window = (
            Window
            .partitionBy(column)
        )

        return (
            F.col(column).isNotNull()
            &
            (
                F.count(
                    F.lit(1)
                )
                .over(duplicate_window)
                > 1
            )
        )

    raise ValueError(
        f"Unsupported rule type: {rule_type}"
    )