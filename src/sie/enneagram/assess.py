"""Main assessment orchestration."""

from __future__ import annotations

from collections import defaultdict

from sie.enneagram.inputs import AssessmentInput
from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.questions import (
    INSTINCT_QUESTIONS,
    get_center_questions,
    get_type_questions,
)
from sie.enneagram.wing_questions import get_wing_questions
from sie.enneagram.rationale import build_reasoning
from sie.enneagram.confidence import (
    LOW_CONFIDENCE_THRESHOLD,
    normalize_shares,
    wing_confidence_detail,
)
from sie.enneagram.scoring import (
    analyze_center_base,
    analyze_type_base,
    gather_supplemental_type,
    merge_type_scores,
    normalize_type_scores,
    refine_primary_type_detailed,
    refine_type_from_supplemental_only,
    resolve_final_center,
    score_center,
    score_episodes,
    score_instinct,
    score_wing_detail,
)
from sie.enneagram.types import (
    CENTER_TYPES,
    GROWTH_PATTERN,
    STRESS_PATTERN,
    Center,
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


def _validate_type_step(
    center: Center,
    type_answers: dict[str, int],
    type_tiebreak_answers: dict[str, int],
    type_tiebreak_pair: tuple[int, int] | None,
    step_name: str,
) -> list[str]:
    errors: list[str] = []
    type_questions = get_type_questions(center)
    errors.extend(_validate_answers(type_questions, type_answers, step_name))
    try:
        type_base = analyze_type_base(center, type_answers)
        if type_base.borderline:
            if type_tiebreak_pair is None:
                errors.append(f"{step_name}: 接戦のため追加質問への回答が必要です")
            else:
                from sie.enneagram.type_tiebreak_questions import get_type_tiebreak_questions

                tb_questions = get_type_tiebreak_questions(center, type_tiebreak_pair)
                errors.extend(
                    _validate_answers(tb_questions, type_tiebreak_answers, f"{step_name}追加")
                )
    except ValueError:
        pass
    return errors


def _question_center(data: AssessmentInput) -> Center:
    return score_center(
        data.center_answers,
        data.center_tiebreak_answers or None,
        data.center_tiebreak_pair,
    )


def _resolve_type_result(data: AssessmentInput, resolved, supplemental_type):
    center = resolved.final_center
    if not resolved.center_changed:
        return refine_primary_type_detailed(
            center,
            data.type_answers,
            supplemental_type,
            data.type_tiebreak_answers or None,
            data.type_tiebreak_pair,
        )
    if data.type_reconfirm_center == center and data.type_reconfirm_answers:
        return refine_primary_type_detailed(
            center,
            data.type_reconfirm_answers,
            supplemental_type,
            data.type_reconfirm_tiebreak_answers or None,
            data.type_reconfirm_tiebreak_pair,
        )
    return refine_type_from_supplemental_only(center, supplemental_type)


def validate_input(data: AssessmentInput) -> list[str]:
    """Return validation errors for an assessment input."""
    errors: list[str] = []
    errors.extend(_validate_answers(get_center_questions(), data.center_answers, "センター判定"))

    try:
        base = analyze_center_base(data.center_answers)
        if base.borderline:
            if data.center_tiebreak_pair is None:
                errors.append("センター追加判定: 接戦のため追加質問への回答が必要です")
            else:
                from sie.enneagram.center_tiebreak_questions import get_center_tiebreak_questions

                tb_questions = get_center_tiebreak_questions(data.center_tiebreak_pair)
                errors.extend(
                    _validate_answers(tb_questions, data.center_tiebreak_answers, "センター追加判定")
                )
    except ValueError:
        pass

    try:
        resolved = resolve_final_center(data)
        center = resolved.final_center
        errors.extend(
            _validate_type_step(
                _question_center(data),
                data.type_answers,
                data.type_tiebreak_answers,
                data.type_tiebreak_pair,
                "タイプ判定",
            )
        )
        if resolved.center_changed:
            if data.type_reconfirm_center != center:
                errors.append(
                    "タイプ再確認: センター調整後のタイプ質問への回答が必要です"
                )
            else:
                errors.extend(
                    _validate_type_step(
                        center,
                        data.type_reconfirm_answers,
                        data.type_reconfirm_tiebreak_answers,
                        data.type_reconfirm_tiebreak_pair,
                        "タイプ再確認",
                    )
                )
        supplemental_type = gather_supplemental_type(data)
        type_result = _resolve_type_result(data, resolved, supplemental_type)
        wing_questions = get_wing_questions(type_result.refined)
        errors.extend(_validate_answers(wing_questions, data.wing_answers, "ウイング判定"))
    except ValueError:
        pass
    errors.extend(_validate_answers(INSTINCT_QUESTIONS, data.instinct_answers, "本能判定"))
    return errors


def run_assessment(data: AssessmentInput) -> EnneagramProfile:
    """Run the full assessment and return an Enneagram profile."""
    errors = validate_input(data)
    if errors:
        raise ValueError("\n".join(errors))

    tiebreak_used = bool(data.center_tiebreak_pair and data.center_tiebreak_answers)
    resolved = resolve_final_center(data)
    center = resolved.final_center
    refined_center = resolved.refined_center
    center_totals = refined_center.totals
    center_confidence = refined_center.confidence
    type_answered_center = resolved.type_answered_center
    center_changed_for_type = resolved.center_changed
    cross_center = resolved.cross_center
    cross_adjusted = resolved.cross_adjusted
    question_center = refined_center.question_center

    type_tiebreak_used = bool(
        data.type_tiebreak_pair
        and data.type_tiebreak_answers
        and not center_changed_for_type
    )
    type_reconfirm_tiebreak_used = bool(
        center_changed_for_type
        and data.type_reconfirm_tiebreak_pair
        and data.type_reconfirm_tiebreak_answers
    )

    _, episode_instinct = score_episodes(data.episodes)
    supplemental_type = gather_supplemental_type(data)

    type_reconfirmed = bool(
        center_changed_for_type
        and data.type_reconfirm_center == center
        and data.type_reconfirm_answers
    )
    type_supplemental_only = center_changed_for_type and not type_reconfirmed

    type_result = _resolve_type_result(data, resolved, supplemental_type)

    primary_type = type_result.refined
    question_primary = type_result.question_primary
    type_totals_in_center = type_result.merged_totals
    type_confidence = type_result.confidence
    type_question_confidence = type_result.question_confidence
    type_adjusted_by_supplemental = type_result.adjusted
    type_borderline = type_result.borderline
    type_low_confidence = (
        type_confidence < LOW_CONFIDENCE_THRESHOLD
        or type_supplemental_only
        or (
            type_borderline
            and not type_tiebreak_used
            and not type_reconfirm_tiebreak_used
        )
    )

    effective_type_answers = (
        data.type_reconfirm_answers
        if type_reconfirmed
        else data.type_answers
    )
    wing, wing_low, wing_high, wing_totals = score_wing_detail(
        primary_type, data.wing_answers, effective_type_answers
    )
    wing_confidence, wing_shares = wing_confidence_detail(
        wing_low, wing_high, wing_totals
    )
    wing_low_confidence = bool(
        wing is not None and wing_confidence < LOW_CONFIDENCE_THRESHOLD
    )

    center_shares = normalize_shares(center_totals)
    center_low_confidence = center_confidence < LOW_CONFIDENCE_THRESHOLD
    type_share_order = CENTER_TYPES[center]
    type_shares_in_center = normalize_shares(
        {t: type_totals_in_center.get(t, 0.0) for t in type_share_order}
    )

    instinct_scores = defaultdict(float)
    for question in INSTINCT_QUESTIONS:
        idx = data.instinct_answers.get(question.id)
        if idx is None:
            continue
        for key, value in question.options[idx].scores.items():
            instinct_scores[key] += value
    for k, v in episode_instinct.items():
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
        center_confidence=center_confidence,
        center_tiebreak_used=tiebreak_used,
        center_tiebreak_pair=data.center_tiebreak_pair,
        center_adjusted_by_supplemental=refined_center.adjusted,
        center_supplemental_totals=refined_center.supplemental_totals,
        center_supplemental_suggested=refined_center.supplemental_suggested,
        question_center=question_center,
        cross_center=cross_center,
        cross_center_adjusted=cross_adjusted,
        type_answered_center=type_answered_center,
        center_changed_for_type=center_changed_for_type,
        type_reconfirmed=type_reconfirmed,
        type_supplemental_only=type_supplemental_only,
        type_tiebreak_used=type_tiebreak_used,
        type_tiebreak_pair=data.type_tiebreak_pair,
        type_reconfirm_tiebreak_used=type_reconfirm_tiebreak_used,
        type_reconfirm_tiebreak_pair=data.type_reconfirm_tiebreak_pair,
        question_primary=question_primary,
        refined_primary=primary_type,
        type_confidence=type_confidence,
        type_question_confidence=type_question_confidence,
        type_question_totals=type_result.question_totals,
        type_adjusted_by_supplemental=type_adjusted_by_supplemental,
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
        center_confidence=center_confidence,
        center_shares=center_shares,
        center_low_confidence=center_low_confidence,
        type_confidence=type_confidence,
        type_question_confidence=type_question_confidence,
        type_shares_in_center=type_shares_in_center,
        type_share_order=type_share_order,
        type_low_confidence=type_low_confidence,
        wing_confidence=wing_confidence,
        wing_shares=wing_shares,
        wing_share_order=(wing_low, wing_high),
        wing_low_confidence=wing_low_confidence,
        center_changed_for_type=center_changed_for_type,
        type_reconfirmed=type_reconfirmed,
        type_supplemental_only=type_supplemental_only,
    )
