from typing import List

from src.quality.models import (
    RuleResult,
)


def print_quality_report(
    results: List[RuleResult],
) -> None:

    print("\n")
    print("=" * 60)
    print("DATA QUALITY RULE RESULTS")
    print("=" * 60)

    passed_count = 0
    failed_count = 0

    for result in results:

        status = (
            "PASS"
            if result.passed
            else "FAIL"
        )

        if result.passed:
            passed_count += 1
        else:
            failed_count += 1

        print("\n")
        print(
            f"Rule: "
            f"{result.rule_id}"
        )

        print(
            f"Type: "
            f"{result.rule_type}"
        )

        print(
            f"Column: "
            f"{result.column}"
        )

        print(
            f"Severity: "
            f"{result.severity}"
        )

        print(
            f"Status: "
            f"{status}"
        )

        print(
            f"Failed Rows: "
            f"{result.failed_count:,}"
        )

        print(
            f"Failure %: "
            f"{result.failure_percentage:.2f}%"
        )

        print(
            f"Condition: "
            f"{result.condition_description}"
        )

    print("\n")
    print("-" * 60)

    print(
        f"Rules Passed: "
        f"{passed_count}"
    )

    print(
        f"Rules Failed: "
        f"{failed_count}"
    )

    print("=" * 60)