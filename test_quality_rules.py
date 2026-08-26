from src.ingestion.data_reader import (
    read_dataset,
)
from src.ingestion.schemas import (
    CUSTOMER_SCHEMA,
)
from src.quality.report_printer import (
    print_quality_report,
)
from src.quality.rule_engine import (
    evaluate_rules,
)
from src.utils.config_loader import (
    load_json_config,
)
from src.utils.spark_session import (
    get_spark_session,
)
from src.quality.result_writer import (
    write_quality_results,
)

spark = get_spark_session(
    "Checkpoint-6-Quality-Test"
)

df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.csv",
    file_format="csv",
    schema=CUSTOMER_SCHEMA,
)

rules_config = load_json_config(
    "config/rules/simple_rules.json"
)

results = evaluate_rules(
    df,
    rules_config,
)
write_quality_results(
    results,
    "output/customer_quality_results.json",
)

print_quality_report(
    results
)

spark.stop()

print(
    "\nQUALITY RULE ENGINE TEST SUCCESSFUL"
)