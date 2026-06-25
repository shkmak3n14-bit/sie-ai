"""Tests for Phase Type-B type tie-breaker and confidence."""

from sie.enneagram.questions import get_type_questions
from sie.enneagram.scoring import (
    TYPE_BORDERLINE_GAP_RATIO,
    analyze_type_base,
    analyze_type_final,
    score_type_in_center,
)
from sie.enneagram.type_tiebreak_questions import (
    get_type_tiebreak_questions,
    normalize_type_pair,
)
from sie.enneagram.types import Center


def _all_zeros(center: Center, value: int = 0) -> dict[str, int]:
    return {q.id: value for q in get_type_questions(center)}


def test_borderline_type_detection_close_scores() -> None:
    type_answers = _all_zeros(Center.BODY, 0)
    for i, q in enumerate(get_type_questions(Center.BODY)):
        if i % 2 == 1:
            type_answers[q.id] = 1
    analysis = analyze_type_base(Center.BODY, type_answers)
    assert analysis.borderline
    assert analysis.tiebreak_pair in ((8, 9), (8, 1), (9, 1))


def test_not_borderline_clear_type_winner() -> None:
    type_answers = _all_zeros(Center.BODY, 0)
    analysis = analyze_type_base(Center.BODY, type_answers)
    assert not analysis.borderline
    assert analysis.primary == 8
    assert analysis.confidence > 0.55


def test_type_tiebreak_resolves_pair() -> None:
    type_answers = _all_zeros(Center.BODY, 0)
    for i, q in enumerate(get_type_questions(Center.BODY)):
        if i % 2 == 1:
            type_answers[q.id] = 1
    base = analyze_type_base(Center.BODY, type_answers)
    pair = base.tiebreak_pair
    assert pair is not None

    tb_questions = get_type_tiebreak_questions(Center.BODY, pair)
    assert len(tb_questions) == 5

    tb_answers = {q.id: 1 for q in tb_questions}
    final = analyze_type_final(Center.BODY, type_answers, tb_answers, pair)
    assert final.primary == pair[1]
    assert final.confidence > base.confidence


def test_normalize_type_pair_order() -> None:
    assert normalize_type_pair(Center.BODY, 9, 8) == (8, 9)
    assert normalize_type_pair(Center.HEART, 4, 2) == (2, 4)
    assert normalize_type_pair(Center.HEAD, 7, 5) == (5, 7)


def test_each_center_pair_has_five_questions() -> None:
    pairs_by_center = {
        Center.BODY: [(8, 9), (8, 1), (9, 1)],
        Center.HEART: [(2, 3), (2, 4), (3, 4)],
        Center.HEAD: [(5, 6), (6, 7), (5, 7)],
    }
    for center, pairs in pairs_by_center.items():
        for pair in pairs:
            assert len(get_type_tiebreak_questions(center, pair)) == 5


def test_type_tiebreak_questions_score_single_type_only() -> None:
    for center in Center:
        for pair in ((8, 9), (8, 1), (9, 1)) if center == Center.BODY else ():
            for q in get_type_tiebreak_questions(center, pair):
                for opt in q.options:
                    assert len(opt.scores) == 1
                    key, value = next(iter(opt.scores.items()))
                    assert key in (str(pair[0]), str(pair[1]))
                    assert value == 3.0


def test_borderline_gap_threshold() -> None:
    assert TYPE_BORDERLINE_GAP_RATIO == 0.15


def test_score_type_in_center_with_tiebreak() -> None:
    type_answers = _all_zeros(Center.HEART, 0)
    primary = score_type_in_center(Center.HEART, type_answers)
    assert primary == 2
