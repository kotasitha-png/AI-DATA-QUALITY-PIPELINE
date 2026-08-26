from typing import Any, Dict


def print_profile_report(
    profile: Dict[str, Any]
) -> None:
    """
    Print a human-readable profiling report.
    """

    print("\n")
    print("=" * 50)
    print("DATA PROFILING REPORT")
    print("=" * 50)

    print(
        f"Rows: "
        f"{profile['row_count']:,}"
    )

    print(
        f"Columns: "
        f"{profile['column_count']}"
    )

    for column in profile["columns"]:

        print("\n")
        print(
            f"COLUMN: {column['name']}"
        )

        print("-" * 50)

        print(
            f"Type: "
            f"{column['data_type']}"
        )

        print(
            f"Null Count: "
            f"{column['null_count']:,}"
        )

        print(
            f"Null %: "
            f"{column['null_percentage']:.2f}%"
        )

        print(
            f"Distinct Count: "
            f"{column['distinct_count']:,}"
        )

        print(
            f"Distinct %: "
            f"{column['distinct_percentage']:.2f}%"
        )

        if "min" in column:

            print(
                f"Min: {column['min']}"
            )

            print(
                f"Max: {column['max']}"
            )

            print(
                f"Mean: {column['mean']}"
            )

    print("\n")
    print("=" * 50)
    print("PROFILING COMPLETE")
    print("=" * 50)