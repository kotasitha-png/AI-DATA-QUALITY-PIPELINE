
from src.profiling.profile_writer import write_profile_json
from src.ingestion.data_reader import (
    read_dataset,
)
from src.ingestion.schemas import (
    CUSTOMER_SCHEMA,
)
from src.profiling.data_profiler import (
    profile_dataframe,
)
from src.profiling.report_printer import (
    print_profile_report,
)
from src.utils.spark_session import (
    get_spark_session,
)


spark = get_spark_session(
    "Checkpoint-5-Profiling-Test"
)

df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.csv",
    file_format="csv",
    schema=CUSTOMER_SCHEMA,
)

profile = profile_dataframe(df)

write_profile_json(
    profile,
    "output/customer_profile.json",
)

print_profile_report(profile)

spark.stop()

print(
    "\nGENERIC PROFILING TEST SUCCESSFUL"
)