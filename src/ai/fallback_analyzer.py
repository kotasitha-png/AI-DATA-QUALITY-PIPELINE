from typing import Any, Dict, List


def build_fallback_analysis(
    summary: Dict[str, Any],
    issues: List[Dict[str, Any]],
) -> str:
    """
    Create a deterministic analysis when an
    external LLM is unavailable.
    """

    lines = []

    lines.append(
        "DATA QUALITY ASSESSMENT"
    )

    lines.append("")

    lines.append(
        f"Overall quality score: "
        f"{summary['overall_quality_score']:.2f}%"
    )

    lines.append(
        f"Risk level: "
        f"{summary['risk_level']}"
    )

    lines.append("")

    if not issues:

        lines.append(
            "No configured quality rules failed."
        )

        return "\n".join(lines)

    lines.append(
        "Highest Priority Issues:"
    )

    for position, issue in enumerate(
        issues[:5],
        start=1,
    ):

        lines.append(
            f"{position}. "
            f"{issue['rule_id']} "
            f"({issue['severity']}) - "
            f"{issue['failed_count']:,} "
            f"failed records "
            f"({issue['failure_percentage']:.2f}%)."
        )

    lines.append("")

    lines.append(
        "Recommended Action:"
    )

    lines.append(
        "Review the highest-severity failed rules, "
        "remediate quarantined records, and rerun "
        "validation before downstream publication."
    )

    return "\n".join(lines)