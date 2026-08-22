from src.ingestion.data_reader import read_dataset
from src.ingestion.schemas import CUSTOMER_SCHEMA
from src.utils.spark_session import get_spark_session


spark = get_spark_session(
    "CSV-To-Parquet"
)

df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.csv",
    file_format="csv",
    schema=CUSTOMER_SCHEMA,
)

output_path = (
    "data/raw/customers_10000.parquet"
)

(
    df.write
    .mode("overwrite")
    .parquet(output_path)
)

print(
    "Parquet dataset created:",
    output_path,
)

spark.stop()