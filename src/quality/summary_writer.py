import json
from pathlib import Path
from typing import Any, Dict, List


def write_quality_summary(
    summary: Dict[str, Any],
    issues: List[Dict[str, Any]],
    output_path: str,
) -> None:

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "summary": summary,
        "issues": issues,
    }

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            payload,
            file,
            indent=2,
        )