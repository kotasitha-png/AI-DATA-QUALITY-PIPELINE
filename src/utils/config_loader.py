import json
from pathlib import Path
from typing import Any, Dict


def load_json_config(config_path: str) -> Dict[str, Any]:
    """
    Load a JSON configuration file and return it as a Python dictionary.
    """

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config