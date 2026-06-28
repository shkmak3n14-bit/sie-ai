"""Cross-center validation using Step 2 type signals and supplemental data."""

from __future__ import annotations

from dataclasses import dataclass

from sie.enneagram.scoring import score_type_totals_in_center
from sie.enneagram.types import CENTER_TYPES, Center

# Best center must exceed selected by this share of total alignment to flag mismatch.
CROSS_CENTER_MISMATCH_RATIO = 0.15

TYPE_ALIGNMENT_QUESTION_WEIGHT = 1.0
TYPE_ALIGNMENT_SUPPLEMENTAL_WEIGHT = 0.5


@dataclass(frozen=True)
class CrossCenterAnalysis:
    """Compare type-pattern alignment across all three centers."""

    alignment_by_center: dict[Center, float]
    best_type_by_center: dict[Center, int]
    best_center: Center
    selected_center: Center
    type_answered_center: Center
    mismatch: bool
    margin_ratio: float


def _supplemental_center_score(
    supplemental_type: dict[int, float],
    center: Center,
) -> float:
    return sum(supplemental_type.get(t, 0.0) for t in CENTER_TYPES[center])


def _best_type_in_center(
    supplemental_type: dict[int, float],
    center: Center,
) -> int:
    types = CENTER_TYPES[center]
    return max(types, key=lambda t: supplemental_type.get(t, 0.0))


def analyze_cross_center_alignment(
    *,
    selected_center: Center,
    type_answered_center: Center,
    type_answers: dict[str, int],
    supplemental_type: dict[int, float],
    type_tiebreak_answers: dict[str, int] | None = None,
    type_tiebreak_pair: tuple[int, int] | None = None,
) -> CrossCenterAnalysis:
    """
    Score each center's type alignment.

    The answered center uses Step 2 question scores; all centers include
    supplemental type signals (episodes, behavior log, self/other gap).
    """
    alignment: dict[Center, float] = {}
    best_type: dict[Center, int] = {}

    for center in Center:
        question_score = 0.0
        if center == type_answered_center:
            totals = score_type_totals_in_center(
                center,
                type_answers,
                type_tiebreak_answers,
                type_tiebreak_pair,
            )
            question_score = max(totals.values()) if totals else 0.0
            if totals:
                best_type[center] = max(totals, key=totals.get)
            else:
                best_type[center] = _best_type_in_center(supplemental_type, center)
        else:
            best_type[center] = _best_type_in_center(supplemental_type, center)

        supplemental_score = _supplemental_center_score(supplemental_type, center)
        alignment[center] = (
            question_score * TYPE_ALIGNMENT_QUESTION_WEIGHT
            + supplemental_score * TYPE_ALIGNMENT_SUPPLEMENTAL_WEIGHT
        )

    ranked = sorted(alignment.items(), key=lambda item: item[1], reverse=True)
    best_center = ranked[0][0]
    selected_score = alignment.get(selected_center, 0.0)
    best_score = ranked[0][1]
    total = sum(alignment.values()) or 1.0
    margin_ratio = (best_score - selected_score) / total if best_center != selected_center else 0.0
    mismatch = (
        best_center != selected_center
        and margin_ratio >= CROSS_CENTER_MISMATCH_RATIO
    )

    return CrossCenterAnalysis(
        alignment_by_center=alignment,
        best_type_by_center=best_type,
        best_center=best_center,
        selected_center=selected_center,
        type_answered_center=type_answered_center,
        mismatch=mismatch,
        margin_ratio=margin_ratio,
    )


def apply_cross_center_adjustment(
    *,
    current_center: Center,
    center_confidence: float,
    cross: CrossCenterAnalysis,
    already_adjusted_by_supplemental: bool,
    low_confidence_threshold: float = 0.55,
) -> tuple[Center, bool]:
    """
    Apply cross-center correction only when confidence is low and not yet adjusted.

    Returns (final_center, was_adjusted).
    """
    if already_adjusted_by_supplemental:
        return current_center, False
    if not cross.mismatch:
        return current_center, False
    if center_confidence >= low_confidence_threshold:
        return current_center, False
    if cross.best_center == current_center:
        return current_center, False
    return cross.best_center, True
