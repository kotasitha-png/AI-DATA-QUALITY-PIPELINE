from src.quality.rule_engine import (
    evaluate_rules,
)


def test_not_null_rule(
    spark,
):

    data = [
        (1, "a@test.com"),
        (2, None),
        (3, "c@test.com"),
    ]

    df = spark.createDataFrame(
        data,
        [
            "id",
            "email",
        ],
    )

    config = {
        "rules": [
            {
                "rule_id": (
                    "EMAIL_NOT_NULL"
                ),
                "type": "not_null",
                "column": "email",
                "severity": "high",
            }
        ]
    }

    results = evaluate_rules(
        df,
        config,
    )

    result = results[0]

    assert (
        result.failed_count
        == 1
    )

    assert (
        result.failure_percentage
        == 33.33
    )


def test_range_rule(
    spark,
):

    data = [
        (1, 25),
        (2, -5),
        (3, 150),
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

    results = evaluate_rules(
        df,
        config,
    )

    assert (
        results[0].failed_count
        == 2
    )