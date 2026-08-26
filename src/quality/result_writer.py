import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from src.quality.models import (
    RuleResult,
)


def write_quality_results(
    results: List[RuleResult],
    output_path: str,
) -> None:

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    serializable_results = [
        asdict(result)
        for result in results
    ]

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            serializable_results,
            file,
            indent=2,
        )