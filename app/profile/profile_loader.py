import json
from pathlib import Path
from typing import Any


PROFILE_PATH = Path(__file__).resolve().parents[2] / "data" / "profile.json"


def load_profile() -> dict[str, Any]:
    """Load the freelancer profile from profile.json."""
    if not PROFILE_PATH.exists():
        raise FileNotFoundError(
            f"Profile file not found: {PROFILE_PATH}"
        )

    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)