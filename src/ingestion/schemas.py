# from pyspark.sql.types import (
#     DoubleType,
#     IntegerType,
#     StringType,
#     StructField,
#     StructType,
# )


# CUSTOMER_SCHEMA = StructType(
#     [
#         StructField(
#             "customer_id",
#             IntegerType(),
#             True,
#         ),
#         StructField(
#             "first_name",
#             StringType(),
#             True,
#         ),
#         StructField(
#             "last_name",
#             StringType(),
#             True,
#         ),
#         StructField(
#             "email",
#             StringType(),
#             True,
#         ),
#         StructField(
#             "age",
#             IntegerType(),
#             True,
#         ),
#         StructField(
#             "state",
#             StringType(),
#             True,
#         ),
#         StructField(
#             "balance",
#             DoubleType(),
#             True,
#         ),
#         StructField(
#             "signup_date",
#             StringType(),
#             True,
#         ),
#     ]
# )
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType
)

CUSTOMER_SCHEMA = StructType([
    StructField("customer_id", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("state", StringType(), True),
    StructField("balance", DoubleType(), True),
    StructField("signup_date", StringType(), True),
])

