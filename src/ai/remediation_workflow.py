from typing import Any, Dict, List

from src.ai.fallback_analyzer import (
    build_fallback_analysis,
)
from src.ai.llm_client import (
    generate_llm_analysis,
)
from src.ai.prompt_builder import (
    build_quality_analysis_prompt,
)


def run_ai_remediation_workflow(
    summary: Dict[str, Any],
    issues: List[Dict[str, Any]],
    use_llm: bool = True,
) -> Dict[str, Any]:
    """
    Run the AI-assisted remediation workflow.

    Workflow:
        findings
        -> prompt
        -> LLM
        -> fallback if necessary
        -> standardized result
    """

    prompt = build_quality_analysis_prompt(
        summary,
        issues,
    )

    analysis = None
    provider = "deterministic_fallback"

    if use_llm:

        try:

            analysis = (
                generate_llm_analysis(
                    prompt
                )
            )

            if analysis:
                provider = "llm"

        except Exception as exc:

            print(
                "LLM unavailable. "
                "Using deterministic fallback."
            )

            print(
                f"Reason: {exc}"
            )

    if not analysis:

        analysis = (
            build_fallback_analysis(
                summary,
                issues,
            )
        )

    return {
        "provider": provider,
        "analysis": analysis,
    }