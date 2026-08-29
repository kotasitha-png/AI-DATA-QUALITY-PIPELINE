from src.ingestion.data_reader import (
    read_dataset,
)
from src.ingestion.schemas import (
    CUSTOMER_SCHEMA,
)
from src.remediation.output_writer import (
    write_quality_outputs,
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
    "Checkpoint-9-Parquet-Outputs"
)

input_path = (
    "data/raw/customers_10000.csv"
)

valid_path = (
    "data/valid/customers"
)

quarantine_path = (
    "data/quarantine/customers"
)

df = read_dataset(
    spark=spark,
    path=input_path,
    file_format="csv",
    schema=CUSTOMER_SCHEMA,
)

config = load_json_config(
    "config/rules/customer_rules.json"
)

classified_df = classify_records(
    df,
    config,
)

valid_df, quarantine_df = (
    split_valid_quarantine(
        classified_df
    )
)

original_count = df.count()
valid_count = valid_df.count()
quarantine_count = (
    quarantine_df.count()
)

write_quality_outputs(
    valid_df=valid_df,
    quarantine_df=quarantine_df,
    valid_path=valid_path,
    quarantine_path=quarantine_path,
)

print("=" * 60)
print("CHECKPOINT 9 — PARQUET OUTPUT")
print("=" * 60)

print(
    f"Input rows: "
    f"{original_count:,}"
)

print(
    f"Valid rows written: "
    f"{valid_count:,}"
)

print(
    f"Quarantine rows written: "
    f"{quarantine_count:,}"
)

print(
    f"Valid output: "
    f"{valid_path}"
)

print(
    f"Quarantine output: "
    f"{quarantine_path}"
)

print("=" * 60)

spark.stop()

print(
    "\nCHECKPOINT 9 WRITE SUCCESSFUL"
)