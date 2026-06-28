"""Tests for Phase D cross-center validation."""

from sie.enneagram.center_crosscheck import (
    CrossCenterAnalysis,
    analyze_cross_center_alignment,
    apply_cross_center_adjustment,
)
from sie.enneagram.questions import get_center_questions, get_type_questions
from sie.enneagram.types import Center


def _all_center_zeros(value: int = 0) -> dict[str, int]:
    return {q.id: value for q in get_center_questions()}


def _body_type_zeros() -> dict[str, int]:
    return {q.id: 0 for q in get_type_questions(Center.BODY)}


def test_cross_center_detects_head_from_supplemental() -> None:
    type_answers: dict[str, int] = {}
    supplemental_type = {5: 20.0, 6: 18.0, 7: 16.0, 8: 1.0, 9: 0.5, 1: 0.5}

    cross = analyze_cross_center_alignment(
        selected_center=Center.BODY,
        type_answered_center=Center.BODY,
        type_answers=type_answers,
        supplemental_type=supplemental_type,
    )

    assert cross.best_center == Center.HEAD
    assert cross.mismatch is True
    assert cross.best_type_by_center[Center.HEAD] in (5, 6, 7)


def test_cross_center_no_adjustment_when_confidence_high() -> None:
    cross = CrossCenterAnalysis(
        alignment_by_center={Center.BODY: 5.0, Center.HEART: 3.0, Center.HEAD: 20.0},
        best_type_by_center={Center.BODY: 8, Center.HEART: 2, Center.HEAD: 6},
        best_center=Center.HEAD,
        selected_center=Center.BODY,
        type_answered_center=Center.BODY,
        mismatch=True,
        margin_ratio=0.45,
    )
    center, adjusted = apply_cross_center_adjustment(
        current_center=Center.BODY,
        center_confidence=0.72,
        cross=cross,
        already_adjusted_by_supplemental=False,
    )
    assert center == Center.BODY
    assert adjusted is False


def test_cross_center_adjustment_when_low_confidence() -> None:
    cross = CrossCenterAnalysis(
        alignment_by_center={Center.BODY: 4.0, Center.HEART: 3.0, Center.HEAD: 18.0},
        best_type_by_center={Center.BODY: 8, Center.HEART: 2, Center.HEAD: 6},
        best_center=Center.HEAD,
        selected_center=Center.BODY,
        type_answered_center=Center.BODY,
        mismatch=True,
        margin_ratio=0.35,
    )
    center, adjusted = apply_cross_center_adjustment(
        current_center=Center.BODY,
        center_confidence=0.52,
        cross=cross,
        already_adjusted_by_supplemental=False,
    )
    assert center == Center.HEAD
    assert adjusted is True


def test_cross_center_skipped_after_supplemental_adjustment() -> None:
    cross = CrossCenterAnalysis(
        alignment_by_center={Center.BODY: 4.0, Center.HEART: 18.0, Center.HEAD: 3.0},
        best_type_by_center={Center.BODY: 8, Center.HEART: 3, Center.HEAD: 5},
        best_center=Center.HEART,
        selected_center=Center.BODY,
        type_answered_center=Center.BODY,
        mismatch=True,
        margin_ratio=0.4,
    )
    center, adjusted = apply_cross_center_adjustment(
        current_center=Center.BODY,
        center_confidence=0.5,
        cross=cross,
        already_adjusted_by_supplemental=True,
    )
    assert center == Center.BODY
    assert adjusted is False


def test_aligned_cross_no_mismatch() -> None:
    type_answers = _body_type_zeros()
    supplemental_type = {8: 5.0, 9: 2.0, 1: 1.0}

    cross = analyze_cross_center_alignment(
        selected_center=Center.BODY,
        type_answered_center=Center.BODY,
        type_answers=type_answers,
        supplemental_type=supplemental_type,
    )
    assert cross.best_center == Center.BODY
    assert cross.mismatch is False
