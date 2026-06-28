"""Tests for Phase C supplemental center scoring."""

from sie.enneagram.inputs import AssessmentInput, BehaviorLog, EpisodeInput, SelfOtherGap
from sie.enneagram.profile import EpisodeSample
from sie.enneagram.questions import get_center_questions
from sie.enneagram.scoring import (
    CENTER_QUESTION_WEIGHT,
    analyze_center_final,
    merge_center_scores,
    refine_center_with_supplemental,
    score_episodes_center,
    score_supplemental_center,
)
from sie.enneagram.types import Center


def _all_zeros(value: int = 0) -> dict[str, int]:
    return {q.id: value for q in get_center_questions()}


def test_episodes_center_keywords() -> None:
    scores = score_episodes_center(
        EpisodeInput(
            recent_conflict="不安で最悪の展開を考える",
            core_values="分析と情報",
            emotion_handling="心配が止まらない",
        )
    )
    assert scores.get("head", 0) > scores.get("body", 0)


def test_merge_center_weights() -> None:
    question = {"body": 40.0, "heart": 20.0, "head": 10.0}
    supplemental = {"body": 0.0, "heart": 10.0, "head": 0.0}
    merged = merge_center_scores(question, supplemental)
    assert merged["body"] == 40.0 * CENTER_QUESTION_WEIGHT
    assert merged["heart"] > 20.0 * CENTER_QUESTION_WEIGHT


def test_supplemental_does_not_flip_clear_winner() -> None:
    from sie.enneagram.scoring import CenterAnalysis

    analysis = CenterAnalysis(
        center=Center.BODY,
        totals={"body": 40.0, "heart": 20.0, "head": 0.0},
        confidence=40.0 / 60.0,
        borderline=False,
        tiebreak_pair=None,
        ranked=(("body", 40.0), ("heart", 20.0), ("head", 0.0)),
    )
    supplemental = {"body": 0.0, "heart": 100.0, "head": 0.0}
    refined = refine_center_with_supplemental(analysis, supplemental)
    assert refined.center == Center.BODY
    assert refined.adjusted is False
    assert refined.supplemental_suggested == Center.HEART


def test_supplemental_can_flip_borderline() -> None:
    center_answers = _all_zeros(0)
    for i in range(1, 13):
        center_answers[f"c{i:02d}"] = 1
    analysis = analyze_center_final(center_answers)
    assert analysis.center == Center.BODY

    supplemental = {"body": 0.0, "heart": 100.0, "head": 0.0}
    refined = refine_center_with_supplemental(analysis, supplemental)
    assert refined.adjusted is True
    assert refined.center == Center.HEART


def test_score_supplemental_center_combines_sources() -> None:
    data = AssessmentInput(
        center_answers={},
        episodes=EpisodeInput(emotion_handling="怒りを抑える"),
        behavior_log=BehaviorLog(work_role=0, relationship_tendency=0, stress_reaction=0),
        self_other_gap=SelfOtherGap(
            self_image={"assertive": 9},
            others_image={"assertive": 9},
        ),
        episode_samples=[
            EpisodeSample(
                event="ケンカ",
                feeling="腹が立つ",
                action="言い返した",
                result="収まった",
            )
        ],
    )
    scores = score_supplemental_center(data)
    assert scores.get("body", 0) > 0
