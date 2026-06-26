"""Tests for body anger pattern (8w9 vs 9, 8w9 vs 8w7)."""

from sie.enneagram.body_anger_questions import (
    BODY_ANGER_TYPE_QUESTIONS,
    score_body_anger_for_wing,
)
from sie.enneagram.questions import get_type_questions
from sie.enneagram.scoring import analyze_type_base, score_wing_detail
from sie.enneagram.types import Center
from sie.enneagram.wing_questions import WING_QUESTIONS_BY_TYPE


def _8w9_anger_type_answers() -> dict[str, int]:
    """Delayed ignition, quiet burn, action at next opportunity (middle option each)."""
    answers = {q.id: 1 for q in BODY_ANGER_TYPE_QUESTIONS}
    return answers


def test_body_anger_questions_in_type_step() -> None:
    ids = [q.id for q in get_type_questions(Center.BODY)]
    assert "ba_01" in ids
    assert "ba_02" in ids
    assert "ba_03" in ids


def test_8w9_anger_pattern_scores_type_8_not_9() -> None:
    type_answers = {q.id: 0 for q in get_type_questions(Center.BODY)}
    type_answers.update(_8w9_anger_type_answers())
    analysis = analyze_type_base(Center.BODY, type_answers)
    assert analysis.totals.get(8, 0) > analysis.totals.get(9, 0)


def test_8w9_anger_pattern_scores_wing_9() -> None:
    wing_scores = score_body_anger_for_wing(_8w9_anger_type_answers())
    assert wing_scores.get(9, 0) > wing_scores.get(7, 0)


def test_8w9_profile_wing9_with_semantic_wing_answers() -> None:
    """8w9-style answers on fixed wing questions + mandatory anger pattern → w9."""
    type_answers = _8w9_anger_type_answers()
    wing_answers: dict[str, int] = {}
    for q in WING_QUESTIONS_BY_TYPE[8]:
        w9_idx = next(
            i
            for i, opt in enumerate(q.options)
            if "9" in opt.scores
        )
        wing_answers[q.id] = w9_idx

    wing, low, high, totals = score_wing_detail(8, wing_answers, type_answers)
    assert (low, high) == (7, 9)
    assert wing == 9
    assert totals["wing_high"] > totals["wing_low"]


def test_8w7_anger_pattern_scores_wing_7() -> None:
    anger_answers = {q.id: 0 for q in BODY_ANGER_TYPE_QUESTIONS}
    wing_scores = score_body_anger_for_wing(anger_answers)
    assert wing_scores.get(7, 0) > wing_scores.get(9, 0)
