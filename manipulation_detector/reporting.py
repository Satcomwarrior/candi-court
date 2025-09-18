"""Reporting utilities for manipulation detection results."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from .models import ManipulationInstance


def generate_comprehensive_report(instances: Iterable[ManipulationInstance]) -> pd.DataFrame:
    """Return a DataFrame summarizing detection results."""
    data = [inst.to_dict() for inst in instances]
    return pd.DataFrame(data)


def export_to_json(instances: Iterable[ManipulationInstance], path: str | Path) -> None:
    """Export detection results to a JSON file."""
    data = [inst.to_dict() for inst in instances]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
