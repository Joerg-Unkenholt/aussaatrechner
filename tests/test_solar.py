from datetime import date

import pytest

from aussaatrechner.solar import day_length_hours


def test_equator_near_equinox_is_about_12_hours():
    value = day_length_hours(0.0, date(2026, 3, 20))
    assert 12.0 <= value <= 12.3


def test_northern_summer_day_longer_than_winter():
    summer = day_length_hours(52.0, date(2026, 6, 21))
    winter = day_length_hours(52.0, date(2026, 12, 21))
    assert summer > winter
    assert summer > 16
    assert winter < 9


def test_invalid_latitude_rejected():
    with pytest.raises(ValueError):
        day_length_hours(91.0, date(2026, 6, 1))
