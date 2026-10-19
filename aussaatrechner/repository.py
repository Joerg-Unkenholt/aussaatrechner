from __future__ import annotations

import json
from pathlib import Path

from .models import Plant, SowingWindow


def load_plants(path: str | Path) -> list[Plant]:
    path = Path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))

    plants: list[Plant] = []
    for item in raw:
        windows = tuple(
            SowingWindow(
                start_month=int(window["start_month"]),
                end_month=int(window["end_month"]),
                method=window["method"],
                source_precision=window["source_precision"],
                source_text=window["source_text"],
                source_url=window["source_url"],
            )
            for window in item["windows"]
        )
        plants.append(
            Plant(
                crop_id=item["crop_id"],
                name_de=item["name_de"],
                scientific_name=item["scientific_name"],
                notes=item["notes"],
                windows=windows,
            )
        )
    return plants
