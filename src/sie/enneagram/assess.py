"""Main assessment orchestration."""

from __future__ import annotations

from collections import defaultdict

from sie.enneagram.inputs import AssessmentInput
from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.questions import (
    CENTER_QUESTIONS,
    INSTINCT_QUESTIONS,
    get_type_questions,
)
from sie.enneagram.wing_questions import get_wing_questions
from sie.enneagram.rationale import build_reasoning
from sie.enneagram.scoring import (
    merge_type_scores,
    normalize_type_scores,
    refine_primary_type,
    score_behavior_log,
    score_center,
    score_center_totals,
    score_episodes,
    score_instinct,
    score_self_other_gap,
    score_type_in_center,
    score_type_totals_in_center,
    score_wing_detail,
)
from sie.enneagram.types import (
    GROWTH_PATTERN,
    STRESS_PATTERN,
    get_type_info,
)


def _validate_answers(
    questions: tuple,
    answers: dict[str, int],
    step_name: str,
) -> list[str]:
    errors: list[str] = []
    for question in questions:
        if question.id not in answers:
            errors.append(f"{step_name}: 質問 {question.id} への回答がありません")
    return errors


def validate_input(data: AssessmentInput) -> list[str]:
    """Return validation errors for an assessment input."""
    errors: list[str] = []
    errors.extend(_validate_answers(CENTER_QUESTIONS, data.center_answers, "センター判定"))

    try:
        center = score_center(data.center_answers)
        type_questions = get_type_questions(center)
        errors.extend(_validate_answers(type_questions, data.type_answers, "タイプ判定"))
    except ValueError:
        pass

    try:
        center = score_center(data.center_answers)
        question_primary = score_type_in_center(center, data.type_answers)
        wing_questions = get_wing_questions(question_primary)
        errors.extend(_validate_answers(wing_questions, data.wing_answers, "ウイング判定"))
    except ValueError:
        pass
    errors.extend(_validate_answers(INSTINCT_QUESTIONS, data.instinct_answers, "本能判定"))
    return errors


def run_assessment(data: AssessmentInput) -> EnneagramProfile:
    """
    Run the full four-step assessment plus supplementary data integration.

    Steps:
    1. Center (body / heart / head)
    2. Primary type within center
    3. Wing
    4. Instinctual variant (sp / so / sx)
    """
    errors = validate_input(data)
    if errors:
        raise ValueError("\n".join(errors))

    center = score_center(data.center_answers)
    center_totals = score_center_totals(data.center_answers)
    question_primary = score_type_in_center(center, data.type_answers)
    type_totals_in_center = score_type_totals_in_center(center, data.type_answers)

    supplemental_type: dict[int, float] = defaultdict(float)
    supplemental_instinct: dict[str, float] = defaultdict(float)

    episode_type, episode_instinct = score_episodes(data.episodes)
    supplemental_type = merge_type_scores(supplemental_type, episode_type)
    for k, v in episode_instinct.items():
        supplemental_instinct[k] += v

    if data.behavior_log is not None:
        supplemental_type = merge_type_scores(
            supplemental_type, score_behavior_log(data.behavior_log)
        )

    if data.self_other_gap is not None:
        supplemental_type = merge_type_scores(
            supplemental_type, score_self_other_gap(data.self_other_gap)
        )

    wing, wing_low, wing_high, wing_totals = score_wing_detail(
        question_primary, data.wing_answers
    )

    primary_type = refine_primary_type(center, question_primary, supplemental_type)

    instinct_scores = defaultdict(float)
    for question in INSTINCT_QUESTIONS:
        idx = data.instinct_answers.get(question.id)
        if idx is None:
            continue
        for key, value in question.options[idx].scores.items():
            instinct_scores[key] += value
    for k, v in supplemental_instinct.items():
        instinct_scores[k] += v * 0.5

    if instinct_scores:
        instinct_variant = max(instinct_scores, key=instinct_scores.get)  # type: ignore[arg-type]
    else:
        instinct_variant = score_instinct(data.instinct_answers)

    type_info = get_type_info(primary_type)
    all_type_scores = merge_type_scores(
        {primary_type: 5.0},
        supplemental_type,
    )
    normalized = normalize_type_scores(all_type_scores)

    reasoning = build_reasoning(
        center=center,
        center_totals=center_totals,
        question_primary=question_primary,
        refined_primary=primary_type,
        type_totals_in_center=type_totals_in_center,
        supplemental_type=dict(supplemental_type),
        wing=wing,
        wing_low=wing_low,
        wing_high=wing_high,
        wing_totals=wing_totals,
        instinct_variant=instinct_variant,
        instinct_totals=dict(instinct_scores),
        normalized_scores=normalized,
    )

    return EnneagramProfile(
        primary_type=primary_type,
        wing=wing,
        scores=normalized,
        summary=type_info.summary,
        strengths=list(type_info.strengths),
        blind_spots=list(type_info.blind_spots),
        stress_pattern=STRESS_PATTERN[primary_type],
        growth_pattern=GROWTH_PATTERN[primary_type],
        instinctual_variant=instinct_variant,  # type: ignore[arg-type]
        core_fear=type_info.core_fear,
        core_desire=type_info.core_desire,
        communication_style=type_info.communication_style,
        conflict_pattern=type_info.conflict_pattern,
        relationship_needs=list(type_info.relationship_needs),
        childhood_wound=type_info.childhood_wound,
        episode_samples=data.episode_samples,
        reasoning=reasoning,
    )
