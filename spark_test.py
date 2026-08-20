from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("AutoDQ-Spark-Test")
    .master("local[*]")
    .getOrCreate()
)

print("================================")
print("SPARK TEST SUCCESSFUL")
print("Spark version:", spark.version)
print("================================")

data = [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
]

df = spark.createDataFrame(
    data,
    ["id", "name"]
)

df.show()

spark.stop()


#######
