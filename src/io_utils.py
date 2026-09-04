"""Load YAML configuration."""

from pathlib import Path

import yaml


def load_config(path: str | Path | None = None) -> dict:
    if path is None:
        path = Path(__file__).resolve().parents[1] / "config" / "default.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
