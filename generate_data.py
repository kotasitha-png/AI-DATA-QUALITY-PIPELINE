import argparse

from src.generators.customer_generator import (
    generate_customer_data,
)


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Generate synthetic customer data "
            "for the AI Data Quality Pipeline."
        )
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=10000,
        help="Number of base rows to generate.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/raw/customers.csv",
        help="Output CSV path.",
    )

    args = parser.parse_args()

    generate_customer_data(
        row_count=args.rows,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()