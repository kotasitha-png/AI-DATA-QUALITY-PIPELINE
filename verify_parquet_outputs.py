from src.ingestion.data_reader import (
    read_dataset,
)
from src.utils.spark_session import (
    get_spark_session,
)


spark = get_spark_session(
    "Checkpoint-9-Readback-Test"
)

valid_df = read_dataset(
    spark=spark,
    path="data/valid/customers",
    file_format="parquet",
)

quarantine_df = read_dataset(
    spark=spark,
    path="data/quarantine/customers",
    file_format="parquet",
)

valid_count = valid_df.count()
quarantine_count = (
    quarantine_df.count()
)

print("=" * 60)
print("PARQUET READBACK VALIDATION")
print("=" * 60)

assert (
    valid_count
    + quarantine_count #### Reconcile persisted records with the original dataset using the verification script
    )

print(f"Total rows read back: {valid_count + quarantine_count:,}")

print(
    f"Valid rows read back: "
    f"{valid_count:,}"
)

print(
    f"Quarantine rows read back: "
    f"{quarantine_count:,}"
)

print("\nVALID SCHEMA")
valid_df.printSchema()

print("\nQUARANTINE SAMPLE")

(
    quarantine_df
    .select(
        "customer_id",
        "_dq_status",
        "_dq_failure_count",
        "_dq_failed_rules",
    )
    .show(
        10,
        truncate=False,
    )
)

spark.stop()

print(
    "\nPARQUET READBACK SUCCESSFUL"
)