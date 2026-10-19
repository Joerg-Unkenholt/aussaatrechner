from datetime import date

from aussaatrechner.engine import (
    cyclic_month_distance_to_window,
    month_in_window,
    recommend,
)
from aussaatrechner.models import Plant, SowingWindow


def build_plant(precision="high"):
    return Plant(
        crop_id="test",
        name_de="Testpflanze",
        scientific_name="Testus plantus",
        notes="",
        windows=(
            SowingWindow(
                start_month=9,
                end_month=10,
                method="protected",
                source_precision=precision,
                source_text="source",
                source_url="https://example.org",
            ),
        ),
    )


def test_month_in_normal_window():
    assert month_in_window(9, 9, 10)
    assert month_in_window(10, 9, 10)
    assert not month_in_window(11, 9, 10)


def test_month_in_wrapping_window():
    assert month_in_window(12, 11, 2)
    assert month_in_window(1, 11, 2)
    assert not month_in_window(6, 11, 2)


def test_cyclic_distance():
    assert cyclic_month_distance_to_window(11, 9, 10) == 1
    assert cyclic_month_distance_to_window(8, 9, 10) == 1
    assert cyclic_month_distance_to_window(1, 9, 10) == 3


def test_matching_window_scores_high():
    rec = recommend([build_plant()], date(2026, 10, 19), "protected")[0]
    assert rec.suitability_score == 85
    assert rec.category == "quellenbasiert passend"


def test_approximation_is_capped():
    rec = recommend(
        [build_plant("approximation")],
        date(2026, 10, 19),
        "protected",
    )[0]
    assert rec.suitability_score == 75
    assert rec.category == "Grenzfall / prüfen"


def test_wrong_method_excluded():
    recs = recommend([build_plant()], date(2026, 10, 19), "outdoor")
    assert recs == []
