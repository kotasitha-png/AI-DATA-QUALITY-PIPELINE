import csv
import random
from datetime import date
from pathlib import Path

from faker import Faker


fake = Faker()


VALID_STATES = [
    "NJ",
    "NY",
    "PA",
    "MA",
    "CT",
    "CA",
    "TX",
    "FL",
    "IL",
    "WA",
]


def generate_customer_data(
    row_count: int,
    output_path: str,
    seed: int = 42,
) -> None:
    """
    Generate synthetic customer data with intentionally injected
    data-quality problems.

    Parameters
    ----------
    row_count:
        Number of base customer rows to generate.

    output_path:
        Destination CSV file.

    seed:
        Random seed so the generated dataset is reproducible.
    """

    random.seed(seed)
    Faker.seed(seed)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for customer_id in range(1, row_count + 1):

        first_name = fake.first_name()
        last_name = fake.last_name()

        email = fake.email()
        age = random.randint(18, 85)
        state = random.choice(VALID_STATES)

        balance = round(
            random.uniform(0, 50000),
            2,
        )

        signup_date = fake.date_between(
            start_date="-5y",
            end_date=date.today(),
        ).isoformat()

        row = {
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "age": age,
            "state": state,
            "balance": balance,
            "signup_date": signup_date,
        }

        rows.append(row)

    inject_quality_issues(rows)

    write_csv(rows, path)

    print("==========================================")
    print("SYNTHETIC DATA GENERATION COMPLETE")
    print("==========================================")
    print(f"Requested base rows: {row_count:,}")
    print(f"Final rows written: {len(rows):,}")
    print(f"Output file: {path}")
    print("==========================================")


def inject_quality_issues(rows: list[dict]) -> None:
    """
    Inject controlled quality problems into the dataset.
    """

    total_rows = len(rows)

    if total_rows == 0:
        return

    # 5% missing emails
    for row in random.sample(
        rows,
        max(1, int(total_rows * 0.05)),
    ):
        row["email"] = None

    # 2% invalid email formats
    for row in random.sample(
        rows,
        max(1, int(total_rows * 0.02)),
    ):
        row["email"] = "invalid-email"

    # 2% invalid ages
    for row in random.sample(
        rows,
        max(1, int(total_rows * 0.02)),
    ):
        row["age"] = random.choice(
            [-10, -1, 130, 250]
        )

    # 2% invalid states
    for row in random.sample(
        rows,
        max(1, int(total_rows * 0.02)),
    ):
        row["state"] = random.choice(
            ["XX", "ZZ", "INVALID"]
        )

    # 1% negative balances
    for row in random.sample(
        rows,
        max(1, int(total_rows * 0.01)),
    ):
        row["balance"] = round(
            random.uniform(-5000, -1),
            2,
        )

    # 1% invalid dates
    for row in random.sample(
        rows,
        max(1, int(total_rows * 0.01)),
    ):
        row["signup_date"] = "not-a-date"

    # Add approximately 1% duplicate rows.
    duplicate_count = max(
        1,
        int(total_rows * 0.01),
    )

    duplicate_rows = random.sample(
        rows,
        duplicate_count,
    )

    rows.extend(
        row.copy()
        for row in duplicate_rows
    )


def write_csv(
    rows: list[dict],
    output_path: Path,
) -> None:

    if not rows:
        raise ValueError(
            "No rows available to write."
        )

    columns = list(rows[0].keys())

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns,
        )

        writer.writeheader()
        writer.writerows(rows)