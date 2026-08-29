from typing import Any, Dict


def print_quality_summary(
    summary: Dict[str, Any],
) -> None:

    print("\n")
    print("=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)

    print(
        f"Total Rows: "
        f"{summary['total_rows']:,}"
    )

    print(
        f"Valid Rows: "
        f"{summary['valid_rows']:,}"
    )

    print(
        f"Quarantined Rows: "
        f"{summary['quarantined_rows']:,}"
    )

    print("-" * 60)

    print(
        f"Row Quality Score: "
        f"{summary['row_quality_score']:.2f}%"
    )

    print(
        f"Weighted Rule Score: "
        f"{summary['weighted_rule_score']:.2f}%"
    )

    print(
        f"Overall Quality Score: "
        f"{summary['overall_quality_score']:.2f}%"
    )

    print(
        f"Risk Level: "
        f"{summary['risk_level']}"
    )

    print("-" * 60)

    print(
        f"Rules Passed: "
        f"{summary['rules_passed']}"
    )

    print(
        f"Rules Failed: "
        f"{summary['rules_failed']}"
    )

    print("=" * 60)