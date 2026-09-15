import json
from pathlib import Path

from src.ingestion.data_reader import (
    read_dataset,
)
from src.ingestion.schemas import (
    CUSTOMER_SCHEMA,
)
from src.profiling.data_profiler import (
    profile_dataframe,
)
from src.quality.rule_engine import (
    evaluate_rules,
)
from src.remediation.record_classifier import (
    classify_records,
    split_valid_quarantine,
)
from src.utils.benchmark import (
    build_benchmark_record,
    measure_operation,
)
from src.utils.config_loader import (
    load_json_config,
)
from src.utils.spark_session import (
    get_spark_session,
)


DATASETS = [
    (
        "10K",
        "data/raw/customers_10000.csv",
    ),
    (
        "100K",
        "data/raw/customers_100000.csv",
    ),
    (
        "1M",
        "data/raw/customers_1000000.csv",
    ),
]


spark = get_spark_session(
    "AutoDQ-Scalability-Benchmark"
)

config = load_json_config(
    "config/rules/customer_rules.json"
)

benchmark_results = []


for label, path in DATASETS:

    if not Path(path).exists():

        print(
            f"Skipping {label}: "
            f"{path} does not exist."
        )

        continue

    print("\n")
    print("=" * 60)

    print(
        f"BENCHMARKING {label}"
    )

    print("=" * 60)

    df, ingestion_time = (
        measure_operation(
            lambda: read_dataset(
                spark=spark,
                path=path,
                file_format="csv",
                schema=CUSTOMER_SCHEMA,
            )
        )
    )

    df.persist()

    row_count, materialize_time = (
        measure_operation(
            lambda: df.count()
        )
    )

    profile, profiling_time = (
        measure_operation(
            lambda: profile_dataframe(
                df
            )
        )
    )

    rule_results, validation_time = (
        measure_operation(
            lambda: evaluate_rules(
                df,
                config,
            )
        )
    )

    classified_df, classification_time = (
        measure_operation(
            lambda: classify_records(
                df,
                config,
            )
        )
    )

    classified_df.persist()

    (
        valid_df,
        quarantine_df,
    ) = split_valid_quarantine(
        classified_df
    )

    _, split_execution_time = (
        measure_operation(
            lambda: (
                valid_df.count(),
                quarantine_df.count(),
            )
        )
    )

    total_time = round(
        materialize_time
        + profiling_time
        + validation_time
        + classification_time
        + split_execution_time,
        3,
    )


    throughput = (
    row_count / total_time
    if total_time > 0
    else 0
    )
    timings = {
        "ingestion_plan_seconds": (
            ingestion_time
        ),
        "materialization_seconds": (
            materialize_time
        ),
        "profiling_seconds": (
            profiling_time
        ),
        "validation_seconds": (
            validation_time
        ),
        "classification_seconds": (
            classification_time
        ),
        "split_execution_seconds": (
            split_execution_time
        ),
        "total_processing_seconds": (
            total_time
        ),
    }

    result = build_benchmark_record(
        dataset=label,
        rows=row_count,
        timings=timings,
    )



    result[
    "throughput_rows_per_second"
        ] = round(
    throughput,
    2,
    )

    benchmark_results.append(
        result
    )

    print(
        f"Rows: {row_count:,}"
    )

    print(
        f"Profiling: "
        f"{profiling_time:.3f}s"
    )

    print(
        f"Validation: "
        f"{validation_time:.3f}s"
    )

    print(
        f"Classification: "
        f"{classification_time:.3f}s"
    )

    print(
        f"Split execution: "
        f"{split_execution_time:.3f}s"
    )

    print(
        f"Total processing: "
        f"{total_time:.3f}s"
    )

    print(
    f"Throughput: "
    f"{throughput:,.2f} rows/second"
    )

    classified_df.unpersist()
    df.unpersist()


Path(
    "output"
).mkdir(
    parents=True,
    exist_ok=True,
)


with open(
    "output/scalability_benchmark.json",
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        benchmark_results,
        file,
        indent=2,
    )


spark.stop()


print("\n")
print("=" * 60)
print("SCALABILITY BENCHMARK COMPLETE")
print("=" * 60)