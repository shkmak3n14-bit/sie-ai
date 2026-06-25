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
from sie.enneagram.center_crosscheck import (
    apply_cross_center_adjustment,
    analyze_cross_center_alignment,
)
from sie.enneagram.rationale import build_reasoning
from sie.enneagram.scoring import (
    analyze_center_base,
    analyze_center_final,
    gather_supplemental_type,
    merge_type_scores,
    normalize_type_scores,
    refine_center_with_supplemental,
    refine_primary_type_detailed,
    RefinedTypeResult,
    score_center,
    score_episodes,
    score_instinct,
    score_supplemental_center,
    score_wing_detail,
)
from sie.enneagram.types import (
    CENTER_TYPES,
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
        center = score_center(
            data.center_answers,
            data.center_tiebreak_answers or None,
            data.center_tiebreak_pair,
        )
        type_questions = get_type_questions(center)
        errors.extend(_validate_answers(type_questions, data.type_answers, "タイプ判定"))
        try:
            from sie.enneagram.scoring import analyze_type_base

            type_base = analyze_type_base(center, data.type_answers)
            if type_base.borderline:
                if data.type_tiebreak_pair is None:
                    errors.append("タイプ追加判定: 接戦のため追加質問への回答が必要です")
                else:
                    from sie.enneagram.type_tiebreak_questions import get_type_tiebreak_questions

                    tb_questions = get_type_tiebreak_questions(
                        center, data.type_tiebreak_pair
                    )
                    errors.extend(
                        _validate_answers(
                            tb_questions, data.type_tiebreak_answers, "タイプ追加判定"
                        )
                    )
        except ValueError:
            pass
        supplemental_type = gather_supplemental_type(data)
        type_result = refine_primary_type_detailed(
            center,
            data.type_answers,
            supplemental_type,
            data.type_tiebreak_answers or None,
            data.type_tiebreak_pair,
        )
        wing_questions = get_wing_questions(type_result.refined)
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

    question_center_analysis = analyze_center_final(
        data.center_answers,
        data.center_tiebreak_answers or None,
        data.center_tiebreak_pair,
    )
    tiebreak_used = bool(data.center_tiebreak_pair and data.center_tiebreak_answers)

    _, episode_instinct = score_episodes(data.episodes)
    supplemental_type = gather_supplemental_type(data)
    supplemental_instinct: dict[str, float] = defaultdict(float)
    for k, v in episode_instinct.items():
        supplemental_instinct[k] += v

    supplemental_center = score_supplemental_center(data)
    refined_center = refine_center_with_supplemental(
        question_center_analysis, supplemental_center
    )
    center = refined_center.center
    center_totals = refined_center.totals
    center_confidence = refined_center.confidence

    type_answered_center = question_center_analysis.center
    type_tiebreak_used = bool(data.type_tiebreak_pair and data.type_tiebreak_answers)
    cross_center = analyze_cross_center_alignment(
        selected_center=center,
        type_answered_center=type_answered_center,
        type_answers=data.type_answers,
        supplemental_type=dict(supplemental_type),
        type_tiebreak_answers=data.type_tiebreak_answers or None,
        type_tiebreak_pair=data.type_tiebreak_pair,
    )
    cross_adjusted = False
    adjusted_center, cross_adjusted = apply_cross_center_adjustment(
        current_center=center,
        center_confidence=center_confidence,
        cross=cross_center,
        already_adjusted_by_supplemental=refined_center.adjusted,
    )
    if cross_adjusted:
        center = adjusted_center

    question_center = refined_center.question_center

    if center == type_answered_center:
        type_result = refine_primary_type_detailed(
            center,
            data.type_answers,
            supplemental_type,
            data.type_tiebreak_answers or None,
            data.type_tiebreak_pair,
        )
    else:
        types_in = CENTER_TYPES[center]
        fallback_primary = max(types_in, key=lambda t: supplemental_type.get(t, 0.0))
        merged = {t: supplemental_type.get(t, 0.0) for t in types_in}
        total = sum(merged.values()) or 1.0
        type_result = RefinedTypeResult(
            refined=fallback_primary,
            question_primary=fallback_primary,
            merged_totals=merged,
            confidence=merged.get(fallback_primary, 0.0) / total,
            adjusted=False,
        )

    primary_type = type_result.refined
    question_primary = type_result.question_primary
    type_totals_in_center = type_result.merged_totals
    type_confidence = type_result.confidence
    type_adjusted_by_supplemental = type_result.adjusted

    wing, wing_low, wing_high, wing_totals = score_wing_detail(
        primary_type, data.wing_answers
    )

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
        type_tiebreak_used=type_tiebreak_used,
        type_tiebreak_pair=data.type_tiebreak_pair,
        question_primary=question_primary,
        refined_primary=primary_type,
        type_confidence=type_confidence,
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
    )
