"""Tests for core fear/desire type questions."""

from sie.enneagram.questions import get_type_questions
from sie.enneagram.scoring import score_type_totals_in_center
from sie.enneagram.type_core_questions import (
    TYPE_CORE_QUESTIONS_BY_CENTER,
    get_type_core_questions,
)
from sie.enneagram.types import CENTER_TYPES, Center


def test_each_center_has_eight_core_questions() -> None:
    for center in Center:
        questions = get_type_core_questions(center)
        assert len(questions) == 8
        categories = {q.category for q in questions}
        assert categories == {"core_fear", "core_desire"}


def test_core_questions_score_single_type_only() -> None:
    for center, questions in TYPE_CORE_QUESTIONS_BY_CENTER.items():
        center_types = {str(t) for t in CENTER_TYPES[center]}
        for q in questions:
            for opt in q.options:
                assert len(opt.scores) == 1
                key, value = next(iter(opt.scores.items()))
                assert key in center_types
                assert value == 2.5


def test_core_questions_discriminate_types_in_center() -> None:
    for center in Center:
        questions = get_type_core_questions(center)
        types = CENTER_TYPES[center]
        for type_idx, type_num in enumerate(types):
            answers = {q.id: type_idx for q in questions}
            totals = score_type_totals_in_center(center, answers)
            assert max(totals, key=totals.get) == type_num


def test_type_question_ids_unique_per_center() -> None:
    for center in Center:
        ids = [q.id for q in get_type_questions(center)]
        assert len(ids) == len(set(ids))
