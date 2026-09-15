from src.remediation.record_classifier import (
    classify_records,
    split_valid_quarantine,
)


def test_valid_quarantine_reconciliation(
    spark,
):

    data = [
        (1, 25),
        (2, -5),
        (3, 50),
    ]

    df = spark.createDataFrame(
        data,
        [
            "id",
            "age",
        ],
    )

    config = {
        "rules": [
            {
                "rule_id": "AGE_RANGE",
                "type": "range",
                "column": "age",
                "min": 0,
                "max": 120,
                "severity": "high",
            }
        ]
    }

    classified = classify_records(
        df,
        config,
    )

    valid, quarantine = (
        split_valid_quarantine(
            classified
        )
    )

    assert valid.count() == 2

    assert (
        quarantine.count()
        == 1
    )

    assert (
        valid.count()
        + quarantine.count()
        == df.count()
    )