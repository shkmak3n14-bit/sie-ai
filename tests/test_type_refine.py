"""Tests for type refinement with supplemental 70/30 weighting."""

import pytest

from sie.enneagram.inputs import AssessmentInput, BehaviorLog, EpisodeInput, SelfOtherGap
from sie.enneagram.questions import get_type_questions
from sie.enneagram.scoring import (
    TYPE_QUESTION_WEIGHT,
    TYPE_SUPPLEMENTAL_WEIGHT,
    gather_supplemental_type,
    merge_type_scores_weighted,
    refine_primary_type_detailed,
)
from sie.enneagram.types import Center


def _all_first_option(center: Center) -> dict[str, int]:
    return {q.id: 0 for q in get_type_questions(center)}


def test_merge_type_scores_weighted_ratio() -> None:
    center = Center.BODY
    question_totals = {8: 10.0, 9: 5.0, 1: 0.0}
    supplemental = {8: 0.0, 9: 30.0, 1: 0.0}
    merged = merge_type_scores_weighted(question_totals, supplemental, center)
    q_sum = 15.0
    scale = q_sum / 30.0
    assert merged[8] == pytest.approx(10.0 * TYPE_QUESTION_WEIGHT)
    assert merged[9] == pytest.approx(
        5.0 * TYPE_QUESTION_WEIGHT + 30.0 * scale * TYPE_SUPPLEMENTAL_WEIGHT
    )
    assert merged[9] > merged[8]


def test_refine_primary_type_can_flip_when_borderline() -> None:
    center = Center.BODY
    question_totals = {8: 10.0, 9: 10.0, 1: 0.0}
    supplemental = {8: 0.0, 9: 20.0, 1: 0.0}
    merged = merge_type_scores_weighted(question_totals, supplemental, center)
    assert max(merged, key=merged.get) == 9

    type_answers = _all_first_option(center)
    for i, q in enumerate(get_type_questions(center)):
        if i % 2 == 1:
            type_answers[q.id] = 1
    result = refine_primary_type_detailed(center, type_answers, supplemental)
    assert result.question_primary in (8, 9)
    assert result.refined == 9
    assert result.adjusted is True
    assert result.confidence > 0


def test_gather_supplemental_type_from_input() -> None:
    data = AssessmentInput(
        episodes=EpisodeInput(
            recent_conflict="正しく改善したい",
            core_values="",
            emotion_handling="",
        ),
        behavior_log=BehaviorLog(work_role=0, relationship_tendency=0, stress_reaction=0),
        self_other_gap=SelfOtherGap(
            self_image={"assertive": 9},
            others_image={"assertive": 3},
        ),
    )
    supplemental = gather_supplemental_type(data)
    assert any(v > 0 for v in supplemental.values())
