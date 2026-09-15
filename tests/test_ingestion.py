import pytest

from src.ingestion.data_reader import (
    read_dataset,
)


def test_read_csv(
    spark,
    tmp_path,
):

    file_path = (
        tmp_path / "sample.csv"
    )

    file_path.write_text(
        "id,name\n"
        "1,Alice\n"
        "2,Bob\n",
        encoding="utf-8",
    )

    df = read_dataset(
        spark=spark,
        path=str(file_path),
        file_format="csv",
    )

    assert df.count() == 2

    assert df.columns == [
        "id",
        "name",
    ]


def test_missing_file(
    spark,
):

    with pytest.raises(
        FileNotFoundError
    ):

        read_dataset(
            spark=spark,
            path=(
                "does_not_exist.csv"
            ),
            file_format="csv",
        )


def test_unsupported_format(
    spark,
    tmp_path,
):

    file_path = (
        tmp_path / "sample.txt"
    )

    file_path.write_text(
        "test",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError
    ):

        read_dataset(
            spark=spark,
            path=str(file_path),
            file_format="excel",
        )