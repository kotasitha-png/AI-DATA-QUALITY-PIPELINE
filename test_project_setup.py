from src.utils.spark_session import get_spark_session
from src.utils.config_loader import load_json_config


print("========================================")
print("CHECKPOINT 2 PROJECT TEST")
print("========================================")

config = load_json_config("config/project_config.json")

print("Project:", config["project_name"])
print("Default input format:", config["input"]["default_format"])
print("Valid output path:", config["output"]["valid_path"])

spark = get_spark_session("Checkpoint-2-Test")

print("Spark version:", spark.version)
print("Application name:", spark.sparkContext.appName)
print("Master:", spark.sparkContext.master)

spark.stop()

print("========================================")
print("PROJECT STRUCTURE TEST SUCCESSFUL")
print("========================================")