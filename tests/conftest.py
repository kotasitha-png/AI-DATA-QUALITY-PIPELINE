import pytest

from src.utils.spark_session import (
    get_spark_session,
)


@pytest.fixture(
    scope="session"
)
def spark():
    """
    Provide one SparkSession for
    the automated test session.
    """

    session = get_spark_session(
        "AutoDQ-Pytest"
    )

    yield session

    session.stop()