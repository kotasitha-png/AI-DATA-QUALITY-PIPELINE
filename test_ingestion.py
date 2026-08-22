from src.ingestion.data_reader import read_dataset
from src.ingestion.schemas import CUSTOMER_SCHEMA
from src.utils.spark_session import get_spark_session


spark = get_spark_session(
    "Checkpoint-4-Ingestion-Test"
)

print("==========================================")
print("CHECKPOINT 4 — DATA INGESTION")
print("==========================================")

df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.csv",
    file_format="csv",
)
df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.parquet",
    file_format="parquet",
)

print("\nSCHEMA")
print("------------------------------------------")

df.printSchema()

print("\nSAMPLE DATA")
print("------------------------------------------")

df.show(
    10,
    truncate=False,
)

row_count = df.count()
column_count = len(df.columns)

print("\nDATASET SUMMARY")
print("------------------------------------------")
print(f"Rows: {row_count:,}")
print(f"Columns: {column_count}")
print(
    "Column names:",
    ", ".join(df.columns),
)

print("==========================================")
print("GENERIC INGESTION TEST SUCCESSFUL")
print("==========================================")

spark.stop()

