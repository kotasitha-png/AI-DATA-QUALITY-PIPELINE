from typing import Any, Dict, List

from src.quality.models import (
    RuleResult,
)


SEVERITY_WEIGHTS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


def calculate_row_quality_score(
    total_rows: int,
    valid_rows: int,
) -> float:
    """
    Percentage of rows that passed every
    configured quality rule.
    """

    if total_rows == 0:
        return 100.0

    score = (
        valid_rows
        / total_rows
        * 100
    )

    return round(score, 2)


def calculate_weighted_rule_score(
    results: List[RuleResult],
) -> float:
    """
    Calculate severity-weighted rule compliance.
    """

    if not results:
        return 100.0

    weighted_score = 0.0
    total_weight = 0.0

    for result in results:

        weight = SEVERITY_WEIGHTS.get(
            result.severity.lower(),
            1,
        )

        compliance_percentage = (
            100
            - result.failure_percentage
        )

        weighted_score += (
            compliance_percentage
            * weight
        )

        total_weight += weight

    if total_weight == 0:
        return 100.0

    return round(
        weighted_score
        / total_weight,
        2,
    )


def calculate_overall_quality_score(
    row_quality_score: float,
    weighted_rule_score: float,
) -> float:
    """
    Blend row-level quality and rule-level quality.

    The MVP gives both equal importance.
    """

    score = (
        row_quality_score
        + weighted_rule_score
    ) / 2

    return round(score, 2)


def classify_risk_level(
    overall_score: float,
) -> str:

    if overall_score >= 95:
        return "LOW"

    if overall_score >= 85:
        return "MEDIUM"

    if overall_score >= 70:
        return "HIGH"

    return "CRITICAL"


def build_quality_summary(
    total_rows: int,
    valid_rows: int,
    quarantine_rows: int,
    results: List[RuleResult],
) -> Dict[str, Any]:

    row_score = (
        calculate_row_quality_score(
            total_rows,
            valid_rows,
        )
    )

    rule_score = (
        calculate_weighted_rule_score(
            results
        )
    )

    overall_score = (
        calculate_overall_quality_score(
            row_score,
            rule_score,
        )
    )

    passed_rules = sum(
        1
        for result in results
        if result.passed
    )

    failed_rules = (
        len(results)
        - passed_rules
    )

    return {
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "quarantined_rows": (
            quarantine_rows
        ),
        "row_quality_score": (
            row_score
        ),
        "weighted_rule_score": (
            rule_score
        ),
        "overall_quality_score": (
            overall_score
        ),
        "risk_level": (
            classify_risk_level(
                overall_score
            )
        ),
        "rules_passed": (
            passed_rules
        ),
        "rules_failed": (
            failed_rules
        ),
    }