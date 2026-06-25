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
    get_type_questions,
    get_wing_questions,
    run_assessment,
    validate_input,
)
from sie.enneagram.scoring import score_center as _score_center, score_type_in_center
from sie.enneagram.types import Center
from sie.enneagram.wing_questions import WING_QUESTIONS_BY_TYPE


def _all_zeros(questions, value: int = 0) -> dict[str, int]:
    return {q.id: value for q in questions}


def _body_type_answers() -> dict[str, int]:
    return _all_zeros(get_type_questions(Center.BODY), 0)


def _wing_answers_for_body_type() -> dict[str, int]:
    center = _score_center(_all_zeros(CENTER_QUESTIONS, 0))
    question_primary = score_type_in_center(center, _body_type_answers())
    return _all_zeros(get_wing_questions(question_primary), 0)


@pytest.fixture
def minimal_input() -> AssessmentInput:
    return AssessmentInput(
        center_answers=_all_zeros(CENTER_QUESTIONS, 0),
        type_answers=_body_type_answers(),
        wing_answers=_wing_answers_for_body_type(),
        instinct_answers=_all_zeros(INSTINCT_QUESTIONS, 0),
        episodes=EpisodeInput(
            recent_conflict="正しく改善したい",
            core_values="責任と誠実さ",
            emotion_handling="怒りを抑える",
        ),
        behavior_log=BehaviorLog(work_role=0, relationship_tendency=4, stress_reaction=0),
        self_other_gap=SelfOtherGap(
            self_image={"assertive": 8, "peaceful": 3},
            others_image={"assertive": 4, "peaceful": 7},
        ),
        episode_samples=[
            EpisodeSample(
                event="職場で方針が乱れた",
                feeling="苛立ち",
                action="ルールを整理した",
                result="落ち着いた",
            )
        ],
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
    answers = _all_zeros(CENTER_QUESTIONS, 0)
    center = _score_center(answers)
    assert center == Center.BODY


def test_question_counts() -> None:
    assert len(CENTER_QUESTIONS) == 15
    assert len(get_type_questions(Center.BODY)) == 9
    assert len(get_type_questions(Center.HEART)) == 9
    assert len(get_type_questions(Center.HEAD)) == 9
    for primary in range(1, 10):
        assert len(WING_QUESTIONS_BY_TYPE[primary]) == 8
    assert len(INSTINCT_QUESTIONS) == 12
