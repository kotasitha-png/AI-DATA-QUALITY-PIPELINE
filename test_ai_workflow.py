import json

from src.ai.remediation_workflow import (
    run_ai_remediation_workflow,
)
from src.ai.result_writer import (
    write_ai_result,
)


with open(
    "output/customer_quality_summary.json",
    "r",
    encoding="utf-8",
) as file:

    quality_data = json.load(file)


summary = quality_data["summary"]
issues = quality_data["issues"]


result = run_ai_remediation_workflow(
    summary=summary,
    issues=issues,
    use_llm=True,
)


print("=" * 60)
print("CHECKPOINT 10 — AI REMEDIATION")
print("=" * 60)

print(
    "Provider:",
    result["provider"],
)

print()

print(
    result["analysis"]
)

write_ai_result(
    result,
    "output/customer_ai_analysis.json",
)

print("=" * 60)
print("CHECKPOINT 10 SUCCESSFUL")
print("=" * 60)