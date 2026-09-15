import json
from typing import Any, Dict, List


def build_quality_analysis_prompt(
    summary: Dict[str, Any],
    issues: List[Dict[str, Any]],
) -> str:
    """
    Build a grounded prompt from deterministic
    data-quality results.

    Raw dataset rows are intentionally not sent
    to the LLM.
    """

    payload = {
        "summary": summary,
        "issues": issues,
    }

    structured_context = json.dumps(
        payload,
        indent=2,
    )

    prompt = f"""
You are a senior data quality and data engineering assistant.

Analyze ONLY the deterministic quality findings supplied below.

Do not invent:
- columns
- rules
- failure counts
- business facts
- source-system details

Return a concise technical assessment with these sections:

1. Executive Summary
2. Highest Priority Issues
3. Potential Downstream Impact
4. Recommended Remediation
5. Prevention Recommendations

Prioritize:
critical severity first,
then high,
then medium,
then low.

DATA QUALITY FINDINGS:

{structured_context}
"""

    return prompt.strip()