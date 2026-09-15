import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def generate_llm_analysis(
    prompt: str,
) -> Optional[str]:
    """
    Generate an LLM response.

    Returns None when API configuration
    is unavailable.
    """

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        return None

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    )

    client = OpenAI(
        api_key=api_key
    )

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text