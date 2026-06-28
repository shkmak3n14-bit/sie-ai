"""Tests for core-emotion center discrimination questions."""

from sie.enneagram.center_core_questions import CENTER_CORE_QUESTIONS
from sie.enneagram.questions import CENTER_QUESTIONS, get_center_questions
from sie.enneagram.scoring import score_center_totals
from sie.enneagram.types import Center


def test_core_questions_score_single_center_only() -> None:
    for q in CENTER_CORE_QUESTIONS:
        assert q.category == "core_emotion"
        for opt in q.options:
            assert len(opt.scores) == 1
            key, value = next(iter(opt.scores.items()))
            assert key in ("body", "heart", "head")
            assert value == 2.5


def test_base_questions_no_mixed_center_scoring() -> None:
    for q in CENTER_QUESTIONS:
        for opt in q.options:
            center_keys = {k for k in opt.scores if k in ("body", "heart", "head")}
            assert len(center_keys) == 1


def test_core_questions_discriminate_centers() -> None:
    body_answers = {q.id: 0 for q in CENTER_CORE_QUESTIONS}
    heart_answers = {q.id: 1 for q in CENTER_CORE_QUESTIONS}
    head_answers = {q.id: 2 for q in CENTER_CORE_QUESTIONS}

    assert max(score_center_totals(body_answers), key=score_center_totals(body_answers).get) == "body"
    assert max(score_center_totals(heart_answers), key=score_center_totals(heart_answers).get) == "heart"
    assert max(score_center_totals(head_answers), key=score_center_totals(head_answers).get) == "head"


def test_all_center_question_ids_unique() -> None:
    ids = [q.id for q in get_center_questions()]
    assert len(ids) == len(set(ids))
