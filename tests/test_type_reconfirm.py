"""Tests for Type-E center-change type reconfirmation."""

from unittest.mock import patch

from sie.enneagram.assess import run_assessment, _resolve_type_result
from sie.enneagram.inputs import AssessmentInput, BehaviorLog, EpisodeInput, SelfOtherGap
from sie.enneagram.profile import EpisodeSample
from sie.enneagram.questions import INSTINCT_QUESTIONS, get_center_questions, get_type_questions
from sie.enneagram.scoring import (
    ResolvedCenter,
    analyze_center_final,
    gather_supplemental_type,
    refine_center_with_supplemental,
    refine_primary_type_detailed,
    resolve_final_center,
)
from sie.enneagram.types import Center
from sie.enneagram.wing_questions import get_wing_questions

import pytest

pytest_plugins = ["tests.test_enneagram"]


def _all_zeros(questions, value: int = 0) -> dict[str, int]:
    return {q.id: value for q in questions}


def _borderline_center_answers() -> dict[str, int]:
    answers = _all_zeros(get_center_questions(), 0)
    for i in range(1, 13):
        answers[f"c{i:02d}"] = 1
    return answers


def _heart_changed_resolved(data: AssessmentInput) -> ResolvedCenter:
    base = resolve_final_center(data)
    question_analysis = analyze_center_final(
        data.center_answers,
        data.center_tiebreak_answers or None,
        data.center_tiebreak_pair,
    )
    refined = refine_center_with_supplemental(
        question_analysis,
        {"body": 0.0, "heart": 80.0, "head": 0.0},
    )
    return ResolvedCenter(
        type_answered_center=Center.BODY,
        final_center=Center.HEART,
        center_changed=True,
        refined_center=refined,
        cross_center=base.cross_center,
        cross_adjusted=False,
    )


def test_resolve_final_center_can_change_after_supplemental() -> None:
    data = AssessmentInput(
        center_answers=_borderline_center_answers(),
        type_answers=_all_zeros(get_type_questions(Center.BODY), 0),
        episodes=EpisodeInput(
            recent_conflict="",
            core_values="愛と承認",
            emotion_handling="評価が気になる",
        ),
        behavior_log=BehaviorLog(work_role=2, relationship_tendency=2, stress_reaction=2),
        self_other_gap=SelfOtherGap(
            self_image={"emotional": 9, "helpful": 9},
            others_image={"emotional": 9, "helpful": 8},
        ),
    )
    resolved = resolve_final_center(data)
    assert resolved.center_changed
    assert resolved.final_center == Center.HEART


def test_run_assessment_with_type_reconfirm(minimal_input: AssessmentInput) -> None:
    heart_type = _all_zeros(get_type_questions(Center.HEART), 0)
    data = AssessmentInput(
        center_answers=minimal_input.center_answers,
        type_answers=minimal_input.type_answers,
        type_reconfirm_center=Center.HEART,
        type_reconfirm_answers=heart_type,
        wing_answers=minimal_input.wing_answers,
        instinct_answers=minimal_input.instinct_answers,
        episodes=minimal_input.episodes,
        behavior_log=minimal_input.behavior_log,
        self_other_gap=minimal_input.self_other_gap,
        episode_samples=minimal_input.episode_samples,
    )
    resolved = _heart_changed_resolved(data)
    supplemental = gather_supplemental_type(data)
    primary = refine_primary_type_detailed(
        Center.HEART, heart_type, supplemental
    ).refined
    data.wing_answers = _all_zeros(get_wing_questions(primary), 0)

    with patch("sie.enneagram.assess.resolve_final_center", return_value=resolved):
        profile = run_assessment(data)

    assert profile.center_changed_for_type
    assert profile.type_reconfirmed
    assert not profile.type_supplemental_only
    assert profile.primary_type in (2, 3, 4)
    assert any("タイプ再確認" in line for line in profile.reasoning)


def test_supplemental_only_when_center_changed_without_reconfirm() -> None:
    data = AssessmentInput(
        center_answers=_all_zeros(get_center_questions(), 0),
        type_answers=_all_zeros(get_type_questions(Center.BODY), 0),
        instinct_answers=_all_zeros(INSTINCT_QUESTIONS, 0),
        episodes=EpisodeInput(core_values="愛", emotion_handling="感情"),
        behavior_log=BehaviorLog(work_role=2, relationship_tendency=2, stress_reaction=2),
        self_other_gap=SelfOtherGap(
            self_image={"emotional": 9},
            others_image={"emotional": 8},
        ),
    )
    resolved = _heart_changed_resolved(data)
    result = _resolve_type_result(data, resolved, gather_supplemental_type(data))
    assert result.question_confidence == 0.0
    assert result.borderline is True
