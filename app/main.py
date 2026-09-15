import json

import pandas as pd
import streamlit as st

from src.ai.remediation_workflow import (
    run_ai_remediation_workflow,
)
from src.ingestion.data_reader import (
    read_dataset,
)
from src.profiling.data_profiler import (
    profile_dataframe,
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
from src.remediation.record_classifier import (
    classify_records,
    split_valid_quarantine,
)
from src.utils.spark_session import (
    get_spark_session,
)
from src.utils.upload_utils import (
    save_uploaded_file,
)


st.set_page_config(
    page_title="AI Data Quality Pipeline",
    layout="wide",
)


st.title(
    "AI Data Quality & Remediation Pipeline"
)

st.caption(
    "PySpark-based profiling, validation, "
    "quarantine, scoring and AI remediation."
)


uploaded_dataset = st.file_uploader(
    "Upload dataset",
    type=[
        "csv",
        "json",
        "parquet",
    ],
)


uploaded_rules = st.file_uploader(
    "Upload quality rules JSON",
    type=["json"],
)


use_ai = st.checkbox(
    "Generate AI remediation recommendations",
    value=True,
)


if (
    uploaded_dataset is not None
    and uploaded_rules is not None
):

    if st.button(
        "Analyze Dataset",
        type="primary",
    ):

        with st.spinner(
            "Running PySpark quality pipeline..."
        ):

            dataset_path = (
                save_uploaded_file(
                    uploaded_dataset,
                    uploaded_dataset.name,
                )
            )

            extension = (
                uploaded_dataset.name
                .rsplit(".", 1)[-1]
                .lower()
            )

            rules_config = json.loads(
                uploaded_rules
                .getvalue()
                .decode("utf-8")
            )

            spark = get_spark_session(
                "AI-DQ-Streamlit"
            )

            try:

                df = read_dataset(
                    spark=spark,
                    path=dataset_path,
                    file_format=extension,
                )

                df.cache()

                profile = (
                    profile_dataframe(df)
                )

                rule_results = (
                    evaluate_rules(
                        df,
                        rules_config,
                    )
                )

                classified_df = (
                    classify_records(
                        df,
                        rules_config,
                    )
                )

                classified_df.cache()

                (
                    valid_df,
                    quarantine_df,
                ) = split_valid_quarantine(
                    classified_df
                )

                total_rows = df.count()
                valid_rows = (
                    valid_df.count()
                )

                quarantine_rows = (
                    quarantine_df.count()
                )

                summary = (
                    build_quality_summary(
                        total_rows=total_rows,
                        valid_rows=valid_rows,
                        quarantine_rows=(
                            quarantine_rows
                        ),
                        results=rule_results,
                    )
                )

                issues = (
                    build_issue_summary(
                        rule_results
                    )
                )

                ai_result = (
                    run_ai_remediation_workflow(
                        summary=summary,
                        issues=issues,
                        use_llm=use_ai,
                    )
                )

                st.success(
                    "Analysis complete."
                )

                col1, col2, col3, col4 = (
                    st.columns(4)
                )

                col1.metric(
                    "Total Rows",
                    f"{total_rows:,}",
                )

                col2.metric(
                    "Valid Rows",
                    f"{valid_rows:,}",
                )

                col3.metric(
                    "Quarantined",
                    f"{quarantine_rows:,}",
                )

                col4.metric(
                    "Quality Score",
                    (
                        f"{summary['overall_quality_score']:.2f}%"
                    ),
                )

                st.subheader(
                    "Dataset Profile"
                )

                profile_table = (
                    pd.DataFrame(
                        profile["columns"]
                    )
                )

                st.dataframe(
                    profile_table,
                    use_container_width=True,
                )

                st.subheader(
                    "Quality Issues"
                )

                if issues:

                    issue_table = (
                        pd.DataFrame(
                            issues
                        )
                    )

                    st.dataframe(
                        issue_table,
                        use_container_width=True,
                    )

                else:

                    st.success(
                        "No configured quality "
                        "rules failed."
                    )

                st.subheader(
                    "Quarantined Records"
                )

                if quarantine_rows > 0:

                    quarantine_sample = (
                        quarantine_df
                        .limit(100)
                        .toPandas()
                    )

                    st.dataframe(
                        quarantine_sample,
                        use_container_width=True,
                    )

                    st.caption(
                        "Showing at most 100 "
                        "quarantined records."
                    )

                else:

                    st.success(
                        "No quarantined records."
                    )

                st.subheader(
                    "AI Remediation Analysis"
                )

                st.caption(
                    f"Analysis provider: "
                    f"{ai_result['provider']}"
                )

                st.markdown(
                    ai_result["analysis"]
                )

            except Exception as exc:

                st.error(
                    f"Pipeline failed: {exc}"
                )

            finally:

                try:
                    classified_df.unpersist()
                except Exception:
                    pass

                try:
                    df.unpersist()
                except Exception:
                    pass

                spark.stop()


else:

    st.info(
        "Upload both a dataset and a "
        "quality-rules JSON file to begin."
    )