from typing import Any, Dict, List

from pyspark.sql import DataFrame

from src.quality.models import RuleResult
from src.quality.rules import (
    evaluate_allowed_values,
    evaluate_not_null,
    evaluate_range,
    evaluate_regex,
    evaluate_unique,
)


RULE_HANDLERS = {
    "not_null": evaluate_not_null,
    "unique": evaluate_unique,
    "range": evaluate_range,
    "regex": evaluate_regex,
    "allowed_values": evaluate_allowed_values,
}


def evaluate_rules(
    df: DataFrame,
    config: Dict[str, Any],
) -> List[RuleResult]:
    """
    Evaluate all configured quality rules
    against a Spark DataFrame.
    """

    results = []

    available_columns = set(
        df.columns
    )

    for rule in config["rules"]:

        rule_type = (
            rule["type"]
            .lower()
        )

        column = rule["column"]

        if column not in available_columns:

            raise ValueError(
                f"Rule "
                f"{rule['rule_id']} "
                f"references missing column: "
                f"{column}"
            )

        handler = RULE_HANDLERS.get(
            rule_type
        )

        if handler is None:

            raise ValueError(
                f"Unsupported quality rule: "
                f"{rule_type}"
            )

        result = handler(
            df,
            rule,
        )

        results.append(result)

    return results