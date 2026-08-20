from pyspark.sql import SparkSession


def get_spark_session(app_name: str = "AI-Data-Quality-Pipeline") -> SparkSession:
    """
    Create or return a SparkSession for the application.

    During local development, Spark runs on all available local CPU cores.
    Later, the same application can be configured to run on a Spark cluster.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark