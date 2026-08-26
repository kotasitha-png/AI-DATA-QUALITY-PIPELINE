import json
from pathlib import Path
from typing import Any, Dict


def write_profile_json(
    profile: Dict[str, Any],
    output_path: str,
) -> None:
    """
    Write profiling results to JSON.
    """

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            profile,
            file,
            indent=2,
            default=str,
        )