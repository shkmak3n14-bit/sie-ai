"""Tests for Enneagram assessment module."""

import pytest

from sie.enneagram import (
    AssessmentInput,
    BehaviorLog,
    CENTER_QUESTIONS,
    EpisodeInput,
    EpisodeSample,
    INSTINCT_QUESTIONS,
    SelfOtherGap,
    get_center_questions,
    get_type_questions,
    get_wing_questions,
    run_assessment,
    validate_input,
)
from sie.enneagram.center_core_questions import CENTER_CORE_QUESTIONS
from sie.enneagram.scoring import (
    gather_supplemental_type,
    refine_primary_type_detailed,
    score_center as _score_center,
)
from sie.enneagram.types import Center
from sie.enneagram.wing_questions import WING_QUESTIONS_BY_TYPE


def _all_zeros(questions, value: int = 0) -> dict[str, int]:
    return {q.id: value for q in questions}


def _body_type_answers() -> dict[str, int]:
    return _all_zeros(get_type_questions(Center.BODY), 0)


def _supplemental_data() -> tuple[EpisodeInput, BehaviorLog, SelfOtherGap, list]:
    return (
        EpisodeInput(
            recent_conflict="正しく改善したい",
            core_values="責任と誠実さ",
            emotion_handling="怒りを抑える",
        ),
        BehaviorLog(work_role=0, relationship_tendency=4, stress_reaction=0),
        SelfOtherGap(
            self_image={"assertive": 8, "peaceful": 3},
            others_image={"assertive": 4, "peaceful": 7},
        ),
        [
            EpisodeSample(
                event="職場で方針が乱れた",
                feeling="苛立ち",
                action="ルールを整理した",
                result="落ち着いた",
            )
        ],
    )


def _wing_answers_for_body_type() -> dict[str, int]:
    center_answers = _all_zeros(get_center_questions(), 0)
    center = _score_center(center_answers)
    type_answers = _body_type_answers()
    episodes, behavior_log, self_other_gap, episode_samples = _supplemental_data()
    data = AssessmentInput(
        center_answers=center_answers,
        type_answers=type_answers,
        episodes=episodes,
        behavior_log=behavior_log,
        self_other_gap=self_other_gap,
        episode_samples=episode_samples,
    )
    supplemental = gather_supplemental_type(data)
    primary = refine_primary_type_detailed(center, type_answers, supplemental).refined
    return _all_zeros(get_wing_questions(primary), 0)


@pytest.fixture
def minimal_input() -> AssessmentInput:
    episodes, behavior_log, self_other_gap, episode_samples = _supplemental_data()
    return AssessmentInput(
        center_answers=_all_zeros(get_center_questions(), 0),
        type_answers=_body_type_answers(),
        wing_answers=_wing_answers_for_body_type(),
        instinct_answers=_all_zeros(INSTINCT_QUESTIONS, 0),
        episodes=episodes,
        behavior_log=behavior_log,
        self_other_gap=self_other_gap,
        episode_samples=episode_samples,
    )


def test_validate_input_complete(minimal_input: AssessmentInput) -> None:
    assert validate_input(minimal_input) == []


def test_validate_input_missing_center_answer() -> None:
    data = AssessmentInput(center_answers={"c01": 0})
    errors = validate_input(data)
    assert any("センター判定" in e for e in errors)


def test_run_assessment_returns_profile(minimal_input: AssessmentInput) -> None:
    profile = run_assessment(minimal_input)
    assert 1 <= profile.primary_type <= 9
    assert profile.wing is not None
    assert profile.instinctual_variant in ("sp", "so", "sx")
    assert profile.summary
    assert profile.stress_pattern in range(1, 10)
    assert profile.growth_pattern in range(1, 10)
    assert len(profile.episode_samples) == 1
    assert len(profile.reasoning) >= 5
    assert any("ウイング" in line for line in profile.reasoning)


def test_center_scoring_body_heavy() -> None:
    answers = _all_zeros(get_center_questions(), 0)
    center = _score_center(answers)
    assert center == Center.BODY


def test_question_counts() -> None:
    assert len(CENTER_QUESTIONS) == 15
    assert len(CENTER_CORE_QUESTIONS) == 8
    assert len(get_center_questions()) == 23
    assert len(get_type_questions(Center.BODY)) == 17
    assert len(get_type_questions(Center.HEART)) == 17
    assert len(get_type_questions(Center.HEAD)) == 17
    for primary in range(1, 10):
        assert len(WING_QUESTIONS_BY_TYPE[primary]) == 8
    assert len(INSTINCT_QUESTIONS) == 12
