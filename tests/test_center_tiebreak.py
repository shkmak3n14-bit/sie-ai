"""Tests for Phase B center tie-breaker and confidence."""

import pytest

from sie.enneagram.center_tiebreak_questions import (
    get_center_tiebreak_questions,
    normalize_center_pair,
)
from sie.enneagram.questions import get_center_questions
from sie.enneagram.scoring import (
    CENTER_BORDERLINE_GAP_RATIO,
    analyze_center_base,
    analyze_center_final,
    score_center,
)
from sie.enneagram.types import Center


def _all_zeros(questions, value: int = 0) -> dict[str, int]:
    return {q.id: value for q in questions}


def test_borderline_detection_close_scores() -> None:
    center_answers = _all_zeros(get_center_questions(), 0)
    for i in range(1, 13):
        center_answers[f"c{i:02d}"] = 1  # heart on c01–c12 → close body/heart gap
    analysis = analyze_center_base(center_answers)
    assert analysis.borderline
    assert analysis.tiebreak_pair == (Center.BODY, Center.HEART)


def test_not_borderline_clear_winner() -> None:
    center_answers = _all_zeros(get_center_questions(), 0)
    analysis = analyze_center_base(center_answers)
    assert not analysis.borderline
    assert analysis.center == Center.BODY
    assert analysis.confidence > 0.55


def test_tiebreak_questions_resolve_pair() -> None:
    center_answers = _all_zeros(get_center_questions(), 0)
    for i in range(1, 13):
        center_answers[f"c{i:02d}"] = 1
    base = analyze_center_base(center_answers)
    pair = base.tiebreak_pair
    assert pair is not None

    tb_questions = get_center_tiebreak_questions(pair)
    assert len(tb_questions) == 5

    tb_answers = {q.id: 1 for q in tb_questions}
    final = analyze_center_final(center_answers, tb_answers, pair)
    assert final.center == Center.HEART
    assert final.confidence > base.confidence


def test_normalize_center_pair_order() -> None:
    assert normalize_center_pair(Center.HEART, Center.BODY) == (Center.BODY, Center.HEART)
    assert normalize_center_pair(Center.HEAD, Center.HEART) == (Center.HEART, Center.HEAD)


def test_tiebreak_each_pair_has_five_questions() -> None:
    pairs = [
        (Center.BODY, Center.HEART),
        (Center.HEART, Center.HEAD),
        (Center.HEAD, Center.BODY),
    ]
    for pair in pairs:
        assert len(get_center_tiebreak_questions(pair)) == 5


def test_borderline_gap_threshold() -> None:
    assert CENTER_BORDERLINE_GAP_RATIO == 0.15
