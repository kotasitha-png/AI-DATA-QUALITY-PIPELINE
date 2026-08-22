# from src.ingestion.data_reader import read_dataset
# from src.utils.spark_session import get_spark_session

# spark = get_spark_session()

# read_dataset(
#     spark,
#     "data/raw/customers_10000.csv",
#     "excel",
# )

#### missing file handling test
from src.ingestion.data_reader import read_dataset

from src.utils.spark_session import get_spark_session

spark = get_spark_session()
read_dataset(
    spark,
    "data/raw/file_that_does_not_exist.csv",
    "csv",
)