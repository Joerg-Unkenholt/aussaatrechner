from __future__ import annotations

from datetime import date

from .models import Plant, Recommendation, SowingWindow


def month_in_window(month: int, start: int, end: int) -> bool:
    if start <= end:
        return start <= month <= end
    return month >= start or month <= end


def cyclic_month_distance_to_window(month: int, start: int, end: int) -> int:
    """Minimum month distance on a 12-month circle to any month in the window."""
    months = [m for m in range(1, 13) if month_in_window(m, start, end)]
    distances = [
        min((month - m) % 12, (m - month) % 12)
        for m in months
    ]
    return min(distances)


def _score_window(month: int, window: SowingWindow) -> tuple[int, str]:
    """Transparent baseline heuristic; this is NOT a probability."""
    if month_in_window(month, window.start_month, window.end_month):
        score = 85
        reason = "Datum liegt im quellenbasierten Aussaatfenster."
    elif cyclic_month_distance_to_window(
        month, window.start_month, window.end_month
    ) == 1:
        score = 45
        reason = (
            "Datum liegt einen Kalendermonat neben dem quellenbasierten "
            "Aussaatfenster. Das ist nur ein Prüfhinweis, keine Empfehlung."
        )
    else:
        score = 10
        reason = "Datum liegt außerhalb des quellenbasierten Aussaatfensters."

    if window.source_precision == "approximation":
        score = min(score, 75)
        reason += " Das Monatsfenster ist eine gekennzeichnete Quelleninterpretation."
    elif window.source_precision == "coarse":
        score = min(score, 65)
        reason += " Die Quelle beschreibt den Zeitraum nur grob."

    return score, reason


def _category(score: int) -> str:
    if score >= 80:
        return "quellenbasiert passend"
    if score >= 40:
        return "Grenzfall / prüfen"
    return "derzeit nicht gestützt"


def recommend(
    plants: list[Plant],
    target_date: date,
    method: str,
    empirical_rates: dict[str, tuple[float | None, int]] | None = None,
) -> list[Recommendation]:
    empirical_rates = empirical_rates or {}
    recommendations: list[Recommendation] = []

    for plant in plants:
        matching_windows = [w for w in plant.windows if w.method == method]
        if not matching_windows:
            continue

        candidates = []
        for window in matching_windows:
            score, reason = _score_window(target_date.month, window)
            candidates.append((score, reason, window))

        score, reason, best_window = max(candidates, key=lambda x: x[0])
        rate, n = empirical_rates.get(plant.crop_id, (None, 0))

        recommendations.append(
            Recommendation(
                crop_id=plant.crop_id,
                name_de=plant.name_de,
                scientific_name=plant.scientific_name,
                suitability_score=score,
                category=_category(score),
                reason=reason,
                source_precision=best_window.source_precision,
                source_url=best_window.source_url,
                source_text=best_window.source_text,
                empirical_success_rate=rate,
                empirical_n=n,
            )
        )

    return sorted(
        recommendations,
        key=lambda rec: (rec.suitability_score, rec.empirical_n),
        reverse=True,
    )
