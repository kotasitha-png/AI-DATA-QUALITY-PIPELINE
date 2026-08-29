from src.ingestion.data_reader import (
    read_dataset,
)
from src.ingestion.schemas import (
    CUSTOMER_SCHEMA,
)
from src.quality.issue_summary import (
    build_issue_summary,
)
from src.quality.rule_engine import (
    evaluate_rules,
)
from src.quality.scoring import (
    build_quality_summary,
)
from src.quality.summary_printer import (
    print_quality_summary,
)
from src.quality.summary_writer import (
    write_quality_summary,
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
    "Checkpoint-8-Quality-Scoring"
)

df = read_dataset(
    spark=spark,
    path="data/raw/customers_10000.csv",
    file_format="csv",
    schema=CUSTOMER_SCHEMA,
)

config = load_json_config(
    "config/rules/customer_rules.json"
)

results = evaluate_rules(
    df,
    config,
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

total_rows = df.count()
valid_rows = valid_df.count()

quarantine_rows = (
    quarantine_df.count()
)

summary = build_quality_summary(
    total_rows=total_rows,
    valid_rows=valid_rows,
    quarantine_rows=quarantine_rows,
    results=results,
)

issues = build_issue_summary(
    results
)

print_quality_summary(
    summary
)

print("\nTOP QUALITY ISSUES")
print("-" * 60)

for issue in issues[:5]:

    print(
        f"{issue['rule_id']} | "
        f"Severity={issue['severity']} | "
        f"Failed={issue['failed_count']:,} | "
        f"Failure={issue['failure_percentage']:.2f}% | "
        f"Impact={issue['impact_score']:.2f}"
    )

write_quality_summary(
    summary,
    issues,
    "output/customer_quality_summary.json",
)

spark.stop()

print(
    "\nCHECKPOINT 8 SUCCESSFUL"
)