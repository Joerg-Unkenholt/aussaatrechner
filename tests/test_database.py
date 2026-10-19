from datetime import date

from aussaatrechner.database import (
    add_observation,
    connect,
    empirical_success,
    list_observations,
)
from aussaatrechner.models import GardenObservation


def make_obs(success: bool):
    return GardenObservation(
        crop_id="spinach_hardy",
        sowing_date=date(2026, 9, 1),
        bed_name="Beet 1",
        method="outdoor",
        success=success,
        harvest_kg=None,
        notes="",
    )


def test_observation_roundtrip(tmp_path):
    conn = connect(tmp_path / "test.db")
    add_observation(conn, make_obs(True))
    rows = list_observations(conn)
    assert len(rows) == 1
    assert rows[0]["success"] == 1
    assert rows[0]["crop_id"] == "spinach_hardy"


def test_empirical_success_hidden_below_five(tmp_path):
    conn = connect(tmp_path / "test.db")
    for _ in range(4):
        add_observation(conn, make_obs(True))
    rate, n = empirical_success(conn, "spinach_hardy")
    assert rate is None
    assert n == 4


def test_empirical_success_from_five_or_more(tmp_path):
    conn = connect(tmp_path / "test.db")
    outcomes = [True, True, True, False, False]
    for outcome in outcomes:
        add_observation(conn, make_obs(outcome))
    rate, n = empirical_success(conn, "spinach_hardy")
    assert n == 5
    assert rate == 0.6
