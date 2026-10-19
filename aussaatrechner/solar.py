from __future__ import annotations

from datetime import date
import calendar
import math


def solar_declination_radians(day: date) -> float:
    """NOAA approximation of solar declination.

    Uses the fractional-year equation with hour=12.
    Reference:
    https://gml.noaa.gov/grad/solcalc/solareqns.PDF
    """
    days_in_year = 366 if calendar.isleap(day.year) else 365
    day_of_year = day.timetuple().tm_yday
    gamma = 2 * math.pi / days_in_year * (day_of_year - 1)

    return (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma)
        + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma)
        + 0.00148 * math.sin(3 * gamma)
    )


def day_length_hours(latitude_deg: float, day: date) -> float:
    """Calculate apparent day length from latitude and date.

    NOAA uses 90.833° zenith for sunrise/sunset to approximate
    atmospheric refraction and the apparent solar disk size.

    This function calculates the interval between apparent sunrise
    and sunset. Longitude is not required for duration.
    """
    if not -90.0 <= latitude_deg <= 90.0:
        raise ValueError("latitude_deg must be between -90 and 90")

    lat = math.radians(latitude_deg)
    decl = solar_declination_radians(day)
    zenith = math.radians(90.833)

    denominator = math.cos(lat) * math.cos(decl)
    if abs(denominator) < 1e-12:
        return 24.0 if math.sin(lat) * math.sin(decl) > 0 else 0.0

    cos_hour_angle = (
        math.cos(zenith) / denominator
        - math.tan(lat) * math.tan(decl)
    )

    if cos_hour_angle <= -1.0:
        return 24.0
    if cos_hour_angle >= 1.0:
        return 0.0

    hour_angle_rad = math.acos(cos_hour_angle)
    hour_angle_deg = math.degrees(hour_angle_rad)
    return 2.0 * hour_angle_deg / 15.0
