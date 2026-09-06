"""
Shared metrics and validation helpers for the v2 pipeline (notebooks 00-05).

Why this module exists (v2 fix #5 - "independent verification that wasn't independent"):
In v1, notebooks 01/03/04/05 each redefined identical copies of `gini`, `jain_index`,
and `repeated_nt_score`. A later notebook re-running the *same* formula and calling it an
"independent check" gave false assurance: it verified copy-paste consistency, not
correctness. Centralizing the formulas here removes the risk of silent drift between
copies. It does NOT, by itself, make downstream checks "independent" in the statistical
sense — see notebook 05 v2, section 2, where this is renamed "internal consistency check"
to match what it actually is.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def require(condition: bool, message: str) -> None:
    """Fail loudly instead of silently continuing on a broken assumption."""
    if not bool(condition):
        raise ValueError(message)


def gini(values) -> float:
    """Gini coefficient of inequality (0 = perfectly equal, 1 = maximally unequal)."""
    values = np.sort(np.asarray(values, dtype=float))
    if values.sum() == 0:
        return np.nan
    count = len(values)
    return (2 * np.sum(np.arange(1, count + 1) * values) / (count * values.sum())) - (count + 1) / count


def jain_index(values) -> float:
    """Jain's fairness index (1 = perfectly equal, 1/n = maximally unequal)."""
    array = np.asarray(values, dtype=float)
    denominator = len(array) * np.square(array).sum()
    return float(np.square(array.sum()) / denominator) if denominator else 1.0


def fairness_metrics(values) -> dict:
    """Bundle of descriptive fairness statistics used throughout the pipeline."""
    values = np.asarray(values, dtype=float)
    squared_sum = np.square(values).sum()
    return {
        "total": int(values.sum()),
        "minimum": int(values.min()),
        "maximum": int(values.max()),
        "mean": float(values.mean()),
        "population_variance": float(values.var(ddof=0)),
        "range": int(values.max() - values.min()),
        "jain_index": jain_index(values),
        "gini": gini(values),
        "zero_count": int((values == 0).sum()),
    }


def repeated_nt_score(schedule: pd.DataFrame, weeks: pd.DataFrame) -> tuple[int, int]:
    """
    Count how many repeated weeks match the first week with the same nT (i.e. are supposed to repeat the
    same rotation pattern) actually have an identical (pharmacy, shift_type, access_mode)
    signature. Returns (matches, total_pairs_checked).
    """
    signatures = {
        week_id: frozenset(zip(group["pharmacy_id"], group["location_id"], group["shift_type"], group["access_mode"]))
        for week_id, group in schedule.groupby("week_id")
    }
    week_to_nt = weeks[["week_id", "nT"]].drop_duplicates()
    pairs = 0
    matches = 0
    for _, nt_group in week_to_nt.groupby("nT"):
        week_ids = nt_group["week_id"].tolist()
        if len(week_ids) > 1:
            pairs += len(week_ids) - 1
            matches += sum(signatures[week_ids[0]] == signatures[week_id] for week_id in week_ids[1:])
    return matches, pairs


def schedule_metrics(schedule: pd.DataFrame, weeks: pd.DataFrame, pharmacies) -> dict:
    """One-stop metrics bundle (total/H24 fairness + repeated-nT integrity) for a schedule."""
    total = schedule.groupby("pharmacy_id").size().reindex(pharmacies, fill_value=0).astype(int)
    h24 = (
        schedule.loc[schedule["shift_type"].eq("H24")]
        .groupby("pharmacy_id").size().reindex(pharmacies, fill_value=0).astype(int)
    )
    repeated_matches, repeated_pairs = repeated_nt_score(schedule, weeks)
    return {
        "assignments": int(len(schedule)),
        **{f"total_{key}": value for key, value in fairness_metrics(total).items()},
        **{f"h24_{key}": value for key, value in fairness_metrics(h24).items()},
        "repeated_matches": repeated_matches,
        "repeated_pairs": repeated_pairs,
    }
