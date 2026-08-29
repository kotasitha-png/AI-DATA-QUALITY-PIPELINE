from typing import Any, Dict, List

from src.quality.models import (
    RuleResult,
)
from src.quality.scoring import (
    SEVERITY_WEIGHTS,
)


def build_issue_summary(
    results: List[RuleResult],
) -> List[Dict[str, Any]]:
    """
    Return failed rules ordered by impact.
    """

    issues = []

    for result in results:

        if result.passed:
            continue

        severity_weight = (
            SEVERITY_WEIGHTS.get(
                result.severity.lower(),
                1,
            )
        )

        impact_score = (
            result.failure_percentage
            * severity_weight
        )

        issues.append(
            {
                "rule_id": (
                    result.rule_id
                ),
                "rule_type": (
                    result.rule_type
                ),
                "column": (
                    result.column
                ),
                "severity": (
                    result.severity
                ),
                "failed_count": (
                    result.failed_count
                ),
                "failure_percentage": (
                    result.failure_percentage
                ),
                "impact_score": round(
                    impact_score,
                    2,
                ),
                "condition": (
                    result.condition_description
                ),
            }
        )

    issues.sort(
        key=lambda issue: (
            issue["impact_score"]
        ),
        reverse=True,
    )

    return issues