from src.quality.scoring import (
    calculate_overall_quality_score,
    calculate_row_quality_score,
)


def test_row_quality_score():

    assert (
        calculate_row_quality_score(
            100,
            95,
        )
        == 95.0
    )


def test_empty_dataset_score():

    assert (
        calculate_row_quality_score(
            0,
            0,
        )
        == 100.0
    )


def test_overall_score():

    assert (
        calculate_overall_quality_score(
            90.0,
            98.0,
        )
        == 94.0
    )