"""Tests for type-specific wing questions."""

from sie.enneagram.wing_questions import WING_QUESTIONS_BY_TYPE, get_wing_questions
from sie.enneagram.scoring import score_wing_detail
from sie.enneagram.types import wing_types


def test_each_type_has_eight_wing_questions() -> None:
    for primary in range(1, 10):
        questions = get_wing_questions(primary)
        assert len(questions) == 8
        wing_low, wing_high = wing_types(primary)
        for q in questions:
            assert q.id.startswith(f"w{primary}_")
            for opt in q.options:
                score_keys = set(opt.scores.keys())
                assert score_keys <= {str(wing_low), str(wing_high)}


def test_type8_wing9_vs_w7() -> None:
    questions = WING_QUESTIONS_BY_TYPE[8]
    w9_answers = {}
    w7_answers = {}
    for q in questions:
        w9_idx = next(
            i for i, opt in enumerate(q.options) if "9" in opt.scores
        )
        w7_idx = next(
            i for i, opt in enumerate(q.options) if "7" in opt.scores
        )
        w9_answers[q.id] = w9_idx
        w7_answers[q.id] = w7_idx

    wing9, low, high, totals9 = score_wing_detail(8, w9_answers)
    wing7, _, _, totals7 = score_wing_detail(8, w7_answers)

    assert (low, high) == (7, 9)
    assert wing9 == 9
    assert wing7 == 7
    assert totals9["wing_high"] > totals9["wing_low"]
    assert totals7["wing_low"] > totals7["wing_high"]
