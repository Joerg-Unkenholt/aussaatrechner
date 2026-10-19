from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

GrowingMethod = Literal["outdoor", "protected"]


@dataclass(frozen=True)
class SowingWindow:
    start_month: int
    end_month: int
    method: GrowingMethod
    source_precision: Literal["high", "approximation", "coarse"]
    source_text: str
    source_url: str

    def __post_init__(self) -> None:
        if not 1 <= self.start_month <= 12:
            raise ValueError("start_month must be between 1 and 12")
        if not 1 <= self.end_month <= 12:
            raise ValueError("end_month must be between 1 and 12")


@dataclass(frozen=True)
class Plant:
    crop_id: str
    name_de: str
    scientific_name: str
    notes: str
    windows: tuple[SowingWindow, ...]


@dataclass(frozen=True)
class Recommendation:
    crop_id: str
    name_de: str
    scientific_name: str
    suitability_score: int
    category: str
    reason: str
    source_precision: str
    source_url: str
    source_text: str
    empirical_success_rate: float | None
    empirical_n: int


@dataclass(frozen=True)
class GardenObservation:
    crop_id: str
    sowing_date: date
    bed_name: str
    method: GrowingMethod
    success: bool
    harvest_kg: float | None = None
    notes: str = ""
