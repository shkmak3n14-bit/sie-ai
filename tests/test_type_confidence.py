"""Tests for Type-C type confidence in scoring and profile."""

import pytest

pytest_plugins = ["tests.test_enneagram"]

from sie.enneagram.confidence import format_confidence_lines
from sie.enneagram.inputs import AssessmentInput
from sie.enneagram.questions import get_type_questions
from sie.enneagram.scoring import (
    TYPE_LOW_CONFIDENCE_THRESHOLD,
    refine_primary_type_detailed,
)
from sie.enneagram.types import Center


def _all_zeros(questions, value: int = 0) -> dict[str, int]:
    return {q.id: value for q in questions}


def test_refined_type_result_includes_question_confidence() -> None:
    center = Center.BODY
    type_answers = _all_zeros(get_type_questions(center), 0)
    result = refine_primary_type_detailed(center, type_answers, {})
    assert result.question_confidence > 0.5
    assert result.confidence > 0.5
    assert sum(result.question_totals.values()) > 0


def test_type_low_confidence_threshold() -> None:
    assert TYPE_LOW_CONFIDENCE_THRESHOLD == 0.55


def test_run_assessment_exposes_type_confidence(minimal_input: AssessmentInput) -> None:
    from sie.enneagram.assess import run_assessment

    profile = run_assessment(minimal_input)
    assert profile.type_confidence > 0
    assert profile.type_question_confidence > 0
    assert isinstance(profile.type_low_confidence, bool)
    assert any("信頼度" in line for line in profile.reasoning)
