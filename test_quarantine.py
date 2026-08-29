from src.ingestion.data_reader import (
    read_dataset,
)
from src.ingestion.schemas import (
    CUSTOMER_SCHEMA,
)
from src.remediation.record_classifier import (
    classify_records,
    split_valid_quarantine,
)
from src.utils.config_loader import (
    load_json_config,
)
from src.utils.spark_session import (
    get_spark_session,
)


spark = get_spark_session(
    "Checkpoint-7-Quarantine-Test"
)

df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.csv",
    file_format="csv",
    schema=CUSTOMER_SCHEMA,
)

rules_config = load_json_config(
    "config/rules/customer_rules.json"
)

classified_df = classify_records(
    df,
    rules_config,
)

valid_df, quarantine_df = (
    split_valid_quarantine(
        classified_df
    )
)

total_count = df.count()
valid_count = valid_df.count()
quarantine_count = (
    quarantine_df.count()
)

print("=" * 60)
print("CHECKPOINT 7 — RECORD CLASSIFICATION")
print("=" * 60)

print(
    f"Total records: "
    f"{total_count:,}"
)

print(
    f"Valid records: "
    f"{valid_count:,}"
)

print(
    f"Quarantined records: "
    f"{quarantine_count:,}"
)

print("\nQUARANTINED SAMPLE")
print("-" * 60)

(
    quarantine_df
    .select(
        "customer_id",
        "email",
        "age",
        "state",
        "balance",
        "_dq_status",
        "_dq_failure_count",
        "_dq_failed_rules",
    )
    .show(
        20,
        truncate=False,
    )
)

assert (
    valid_count
    + quarantine_count
    == total_count
)

spark.stop()

print(
    "\nCHECKPOINT 7 SUCCESSFUL"
)