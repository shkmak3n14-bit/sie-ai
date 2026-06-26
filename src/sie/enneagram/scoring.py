"""Scoring logic for the Enneagram assessment."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from sie.enneagram.inputs import AssessmentInput, BehaviorLog, EpisodeInput, SelfOtherGap
from sie.enneagram.profile import EpisodeSample, InstinctualVariant
from sie.enneagram.questions import (
    CENTER_TYPE_QUESTIONS,
    INSTINCT_QUESTIONS,
    Question,
    get_center_questions,
    get_type_questions,
)
from sie.enneagram.wing_questions import get_wing_questions
from sie.enneagram.types import CENTER_TYPES, Center, wing_types

CENTER_BORDERLINE_GAP_RATIO = 0.15
TYPE_BORDERLINE_GAP_RATIO = 0.15
TYPE_LOW_CONFIDENCE_THRESHOLD = 0.55
CENTER_QUESTION_WEIGHT = 0.7
CENTER_SUPPLEMENTAL_WEIGHT = 0.3
TYPE_QUESTION_WEIGHT = 0.7
TYPE_SUPPLEMENTAL_WEIGHT = 0.3


def _score_from_answers(
    questions: tuple[Question, ...],
    answers: dict[str, int],
    score_keys: tuple[str, ...] | None = None,
) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)

    for question in questions:
        option_index = answers.get(question.id)
        if option_index is None:
            continue
        if option_index < 0 or option_index >= len(question.options):
            continue

        option = question.options[option_index]
        for key, value in option.scores.items():
            if score_keys is None or key in score_keys:
                totals[key] += value

    return dict(totals)


def _winner(scores: dict[str, float]) -> str:
    if not scores:
        raise ValueError("スコアが空です。回答を確認してください。")
    return max(scores, key=scores.get)


@dataclass(frozen=True)
class CenterAnalysis:
    """Result of center scoring with confidence and borderline detection."""

    center: Center
    totals: dict[str, float]
    confidence: float
    borderline: bool
    tiebreak_pair: tuple[Center, Center] | None
    ranked: tuple[tuple[str, float], ...]


def _center_gap_ratio(totals: dict[str, float]) -> float:
    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    if len(ranked) < 2:
        return 1.0
    total = sum(totals.values()) or 1.0
    return (ranked[0][1] - ranked[1][1]) / total


def merge_center_scores(
    question_totals: dict[str, float],
    supplemental_totals: dict[str, float],
) -> dict[str, float]:
    """Blend question-based and supplemental center scores (70% / 30%)."""
    supp_sum = sum(supplemental_totals.values())
    if supp_sum <= 0:
        return dict(question_totals)

    q_sum = sum(question_totals.values()) or 1.0
    scale = q_sum / supp_sum
    merged: dict[str, float] = {}
    for key in ("body", "heart", "head"):
        merged[key] = (
            question_totals.get(key, 0) * CENTER_QUESTION_WEIGHT
            + supplemental_totals.get(key, 0) * scale * CENTER_SUPPLEMENTAL_WEIGHT
        )
    return merged


@dataclass(frozen=True)
class RefinedCenterResult:
    """Center after optional supplemental adjustment."""

    center: Center
    totals: dict[str, float]
    confidence: float
    question_center: Center
    question_totals: dict[str, float]
    supplemental_totals: dict[str, float]
    adjusted: bool
    supplemental_suggested: Center | None


def refine_center_with_supplemental(
    question_analysis: CenterAnalysis,
    supplemental_totals: dict[str, float],
) -> RefinedCenterResult:
    """
    Apply supplemental center signals with a 70/30 blend.

    The center may change only when the question-based gap is borderline (≤15%).
    """
    question_center = question_analysis.center
    question_totals = question_analysis.totals
    supp_sum = sum(supplemental_totals.values())

    if supp_sum <= 0:
        return RefinedCenterResult(
            center=question_center,
            totals=question_totals,
            confidence=question_analysis.confidence,
            question_center=question_center,
            question_totals=question_totals,
            supplemental_totals={},
            adjusted=False,
            supplemental_suggested=None,
        )

    merged = merge_center_scores(question_totals, supplemental_totals)
    merged_winner = Center(_winner(merged))
    allow_flip = _center_gap_ratio(question_totals) <= CENTER_BORDERLINE_GAP_RATIO

    if merged_winner != question_center and not allow_flip:
        merged_winner_key = merged_winner.value
        ranked = tuple(sorted(question_totals.items(), key=lambda item: item[1], reverse=True))
        total = sum(question_totals.values()) or 1.0
        return RefinedCenterResult(
            center=question_center,
            totals=question_totals,
            confidence=ranked[0][1] / total,
            question_center=question_center,
            question_totals=question_totals,
            supplemental_totals=supplemental_totals,
            adjusted=False,
            supplemental_suggested=Center(merged_winner_key),
        )

    final_totals = merged
    final_center = merged_winner
    ranked = tuple(sorted(final_totals.items(), key=lambda item: item[1], reverse=True))
    total = sum(final_totals.values()) or 1.0
    adjusted = final_center != question_center

    return RefinedCenterResult(
        center=final_center,
        totals=final_totals,
        confidence=ranked[0][1] / total,
        question_center=question_center,
        question_totals=question_totals,
        supplemental_totals=supplemental_totals,
        adjusted=adjusted,
        supplemental_suggested=None,
    )


@dataclass(frozen=True)
class ResolvedCenter:
    """Center after Phase C supplemental merge and Phase D cross-check."""

    type_answered_center: Center
    final_center: Center
    center_changed: bool
    refined_center: RefinedCenterResult
    cross_center: "CrossCenterAnalysis"
    cross_adjusted: bool


def resolve_final_center(data: AssessmentInput) -> ResolvedCenter:
    """Run Phase C/D center pipeline for UI preview and assessment."""
    from sie.enneagram.center_crosscheck import (
        CrossCenterAnalysis,
        analyze_cross_center_alignment,
        apply_cross_center_adjustment,
    )

    question_analysis = analyze_center_final(
        data.center_answers,
        data.center_tiebreak_answers or None,
        data.center_tiebreak_pair,
    )
    type_answered_center = question_analysis.center
    supplemental_center = score_supplemental_center(data)
    refined = refine_center_with_supplemental(question_analysis, supplemental_center)
    center = refined.center

    supplemental_type = gather_supplemental_type(data)
    cross = analyze_cross_center_alignment(
        selected_center=center,
        type_answered_center=type_answered_center,
        type_answers=data.type_answers,
        supplemental_type=supplemental_type,
        type_tiebreak_answers=data.type_tiebreak_answers or None,
        type_tiebreak_pair=data.type_tiebreak_pair,
    )
    cross_adjusted = False
    adjusted_center, cross_adjusted = apply_cross_center_adjustment(
        current_center=center,
        center_confidence=refined.confidence,
        cross=cross,
        already_adjusted_by_supplemental=refined.adjusted,
    )
    if cross_adjusted:
        center = adjusted_center

    return ResolvedCenter(
        type_answered_center=type_answered_center,
        final_center=center,
        center_changed=(center != type_answered_center),
        refined_center=refined,
        cross_center=cross,
        cross_adjusted=cross_adjusted,
    )


def score_center_base_totals(center_answers: dict[str, int]) -> dict[str, float]:
    """Score Step 1 base + core center questions only."""
    return _score_from_answers(get_center_questions(), center_answers, ("body", "heart", "head"))


def score_center_totals(
    center_answers: dict[str, int],
    tiebreak_answers: dict[str, int] | None = None,
    tiebreak_pair: tuple[Center, Center] | None = None,
) -> dict[str, float]:
    """Score all center answers, optionally including tie-breaker questions."""
    totals: dict[str, float] = defaultdict(float)
    for key, value in score_center_base_totals(center_answers).items():
        totals[key] += value

    if tiebreak_answers and tiebreak_pair:
        from sie.enneagram.center_tiebreak_questions import get_center_tiebreak_questions

        questions = get_center_tiebreak_questions(tiebreak_pair)
        keys = (tiebreak_pair[0].value, tiebreak_pair[1].value)
        for key, value in _score_from_answers(questions, tiebreak_answers, keys).items():
            totals[key] += value

    return dict(totals)


def analyze_center_base(center_answers: dict[str, int]) -> CenterAnalysis:
    """Analyze center scores from Step 1 only; detect borderline pairs."""
    from sie.enneagram.center_tiebreak_questions import normalize_center_pair

    totals = score_center_base_totals(center_answers)
    if not totals:
        raise ValueError("スコアが空です。回答を確認してください。")

    ranked = tuple(sorted(totals.items(), key=lambda item: item[1], reverse=True))
    winner_key = ranked[0][0]
    total = sum(totals.values()) or 1.0
    confidence = ranked[0][1] / total

    gap_ratio = (ranked[0][1] - ranked[1][1]) / total if len(ranked) > 1 else 1.0
    borderline = gap_ratio <= CENTER_BORDERLINE_GAP_RATIO
    tiebreak_pair = None
    if borderline and len(ranked) > 1:
        tiebreak_pair = normalize_center_pair(Center(ranked[0][0]), Center(ranked[1][0]))

    return CenterAnalysis(
        center=Center(winner_key),
        totals=totals,
        confidence=confidence,
        borderline=borderline,
        tiebreak_pair=tiebreak_pair,
        ranked=ranked,
    )


def analyze_center_final(
    center_answers: dict[str, int],
    tiebreak_answers: dict[str, int] | None = None,
    tiebreak_pair: tuple[Center, Center] | None = None,
) -> CenterAnalysis:
    """Analyze center scores including optional tie-breaker answers."""
    totals = score_center_totals(center_answers, tiebreak_answers, tiebreak_pair)
    if not totals:
        raise ValueError("スコアが空です。回答を確認してください。")

    ranked = tuple(sorted(totals.items(), key=lambda item: item[1], reverse=True))
    winner_key = ranked[0][0]
    total = sum(totals.values()) or 1.0
    confidence = ranked[0][1] / total

    return CenterAnalysis(
        center=Center(winner_key),
        totals=totals,
        confidence=confidence,
        borderline=False,
        tiebreak_pair=tiebreak_pair,
        ranked=ranked,
    )


def score_center(
    center_answers: dict[str, int],
    tiebreak_answers: dict[str, int] | None = None,
    tiebreak_pair: tuple[Center, Center] | None = None,
) -> Center:
    totals = score_center_totals(center_answers, tiebreak_answers, tiebreak_pair)
    winner = _winner(totals)
    return Center(winner)


@dataclass(frozen=True)
class TypeAnalysis:
    """Result of type scoring within a center with borderline detection."""

    primary: int
    totals: dict[int, float]
    confidence: float
    borderline: bool
    tiebreak_pair: tuple[int, int] | None
    ranked: tuple[tuple[int, float], ...]


def score_type_base_totals(center: Center, answers: dict[str, int]) -> dict[int, float]:
    """Score Step 2 type questions only (no tie-breaker)."""
    questions = get_type_questions(center)
    type_keys = tuple(str(t) for t in CENTER_TYPES[center])
    totals = _score_from_answers(questions, answers, type_keys)
    return {int(k): v for k, v in totals.items()}


def score_type_totals_in_center(
    center: Center,
    answers: dict[str, int],
    tiebreak_answers: dict[str, int] | None = None,
    tiebreak_pair: tuple[int, int] | None = None,
) -> dict[int, float]:
    """Score type answers, optionally including tie-breaker questions."""
    totals: dict[int, float] = defaultdict(float)
    for t, v in score_type_base_totals(center, answers).items():
        totals[t] += v

    if tiebreak_answers and tiebreak_pair:
        from sie.enneagram.type_tiebreak_questions import get_type_tiebreak_questions

        questions = get_type_tiebreak_questions(center, tiebreak_pair)
        keys = (str(tiebreak_pair[0]), str(tiebreak_pair[1]))
        for key, value in _score_from_answers(questions, tiebreak_answers, keys).items():
            totals[int(key)] += value

    return dict(totals)


def analyze_type_base(center: Center, type_answers: dict[str, int]) -> TypeAnalysis:
    """Analyze type scores from Step 2 only; detect borderline pairs."""
    from sie.enneagram.type_tiebreak_questions import normalize_type_pair

    totals = score_type_base_totals(center, type_answers)
    if not totals:
        types = CENTER_TYPES[center]
        return TypeAnalysis(
            primary=types[0],
            totals={},
            confidence=0.0,
            borderline=False,
            tiebreak_pair=None,
            ranked=(),
        )

    ranked = tuple(sorted(totals.items(), key=lambda item: item[1], reverse=True))
    primary = ranked[0][0]
    total = sum(totals.values()) or 1.0
    confidence = ranked[0][1] / total

    gap_ratio = (ranked[0][1] - ranked[1][1]) / total if len(ranked) > 1 else 1.0
    borderline = gap_ratio <= TYPE_BORDERLINE_GAP_RATIO
    tiebreak_pair = None
    if borderline and len(ranked) > 1:
        tiebreak_pair = normalize_type_pair(center, ranked[0][0], ranked[1][0])

    return TypeAnalysis(
        primary=primary,
        totals=totals,
        confidence=confidence,
        borderline=borderline,
        tiebreak_pair=tiebreak_pair,
        ranked=ranked,
    )


def analyze_type_final(
    center: Center,
    type_answers: dict[str, int],
    tiebreak_answers: dict[str, int] | None = None,
    tiebreak_pair: tuple[int, int] | None = None,
) -> TypeAnalysis:
    """Analyze type scores including optional tie-breaker answers."""
    totals = score_type_totals_in_center(
        center, type_answers, tiebreak_answers, tiebreak_pair
    )
    if not totals:
        types = CENTER_TYPES[center]
        return TypeAnalysis(
            primary=types[0],
            totals={},
            confidence=0.0,
            borderline=False,
            tiebreak_pair=tiebreak_pair,
            ranked=(),
        )

    ranked = tuple(sorted(totals.items(), key=lambda item: item[1], reverse=True))
    primary = ranked[0][0]
    total = sum(totals.values()) or 1.0
    confidence = ranked[0][1] / total

    return TypeAnalysis(
        primary=primary,
        totals=totals,
        confidence=confidence,
        borderline=False,
        tiebreak_pair=tiebreak_pair,
        ranked=ranked,
    )


def score_type_in_center(
    center: Center,
    answers: dict[str, int],
    tiebreak_answers: dict[str, int] | None = None,
    tiebreak_pair: tuple[int, int] | None = None,
) -> int:
    totals = score_type_totals_in_center(
        center, answers, tiebreak_answers, tiebreak_pair
    )
    if not totals:
        raise ValueError("スコアが空です。回答を確認してください。")
    return max(totals, key=totals.get)


def score_wing_detail(
    primary_type: int,
    answers: dict[str, int],
    type_answers: dict[str, int] | None = None,
) -> tuple[int, int, int, dict[str, float]]:
    """Return (chosen_wing, wing_low, wing_high, wing_low/high totals)."""
    wing_low, wing_high = wing_types(primary_type)
    questions = get_wing_questions(primary_type)
    type_keys = (str(wing_low), str(wing_high))
    totals_raw = _score_from_answers(questions, answers, type_keys)
    totals = {
        "wing_low": totals_raw.get(str(wing_low), 0),
        "wing_high": totals_raw.get(str(wing_high), 0),
    }
    if primary_type == 8 and type_answers:
        from sie.enneagram.body_anger_questions import score_body_anger_for_wing

        for wing_num, score in score_body_anger_for_wing(type_answers).items():
            key = "wing_low" if wing_num == wing_low else "wing_high"
            totals[key] += score
    if not totals_raw and not any(totals.values()):
        return wing_low, wing_low, wing_high, totals
    wing = wing_low if totals["wing_low"] >= totals["wing_high"] else wing_high
    return wing, wing_low, wing_high, totals


def score_wing(primary_type: int, answers: dict[str, int]) -> int:
    wing, _, _, _ = score_wing_detail(primary_type, answers)
    return wing


def score_instinct(answers: dict[str, int]) -> InstinctualVariant:
    totals = _score_from_answers(INSTINCT_QUESTIONS, answers, ("sp", "so", "sx"))
    winner = _winner(totals)
    return winner  # type: ignore[return-value]


def _keyword_score(text: str, keywords: tuple[str, ...], weight: float = 0.3) -> float:
    if not text.strip():
        return 0.0
    normalized = text.lower()
    hits = sum(1 for kw in keywords if kw in normalized)
    return hits * weight


# Keyword hints per type for free-text episode analysis
_TYPE_KEYWORDS: dict[int, tuple[str, ...]] = {
    1: ("正しい", "完璧", "改善", "ルール", "批判", "怒り", "責任"),
    2: ("助ける", "必要", "愛", "与える", "感謝", "拒絶", "世話"),
    3: ("成功", "成果", "評価", "効率", "認め", "目標", "達成"),
    4: ("特別", "意味", "孤独", "芸術", "感情", "本物", "欠け"),
    5: ("分析", "理解", "一人", "距離", "知識", "観察", "無能"),
    6: ("不安", "安全", "信頼", "確認", "最悪", "忠実", "リスク"),
    7: ("楽しい", "可能性", "逃避", "計画", "刺激", "退屈", "自由"),
    8: ("強い", "支配", "正義", "率直", "弱さ", "コントロール", "挑戦"),
    9: ("平和", "調和", "積極", "優先", "受け入れ", "対立", "穏やか"),
}

_CENTER_KEYWORDS: dict[Center, tuple[str, ...]] = {
    Center.BODY: ("怒り", "体", "即座", "正しい", "平和", "硬い", "イライラ", "腹"),
    Center.HEART: ("評価", "愛", "必要", "感情", "承認", "意味", "恥", "比較"),
    Center.HEAD: ("不安", "分析", "可能性", "リスク", "考える", "情報", "心配", "最悪"),
}

_BEHAVIOR_WORK_CENTER: tuple[Center, ...] = (
    Center.BODY,   # リーダー
    Center.HEART,  # 助ける
    Center.HEAD,   # 調べる
    Center.HEART,  # 成果
    Center.BODY,   # 調整・平和
)

_BEHAVIOR_RELATION_CENTER: tuple[Center, ...] = (
    Center.HEAD,   # 少数深く
    Center.HEART,  # 広く
    Center.HEAD,   # 距離を保つ
    Center.HEART,  # 評価を気にする
    Center.BODY,   # 平和
)

_BEHAVIOR_STRESS_CENTER: tuple[Center, ...] = (
    Center.BODY,   # type 1 stress → 8 map index 0 → type 1 body
    Center.HEART,  # type 2
    Center.HEART,  # type 3
    Center.HEART,  # type 4
    Center.HEAD,   # type 5
    Center.HEAD,   # type 6
    Center.HEAD,   # type 7
    Center.BODY,   # type 8
    Center.BODY,   # type 9
)

_TRAIT_CENTER_WEIGHTS: dict[str, dict[Center, float]] = {
    "assertive": {Center.BODY: 2.0},
    "emotional": {Center.HEART: 2.0},
    "analytical": {Center.HEAD: 2.0},
    "helpful": {Center.HEART: 1.5},
    "peaceful": {Center.BODY: 1.5},
    "ambitious": {Center.HEART: 1.0, Center.BODY: 0.5},
    "unique": {Center.HEART: 1.5},
    "cautious": {Center.HEAD: 2.0},
}

_INSTINCT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "sp": ("お金", "健康", "安全", "備え", "生活", "住居", "節約"),
    "so": ("所属", "役割", "評価", "グループ", "立場", "ネットワーク"),
    "sx": ("親密", "一人", "情熱", "深い", "特別", "関係"),
}


def score_episode_text_for_center(text: str) -> dict[str, float]:
    """Score free text toward body / heart / head centers."""
    scores: dict[str, float] = defaultdict(float)
    for center, keywords in _CENTER_KEYWORDS.items():
        scores[center.value] += _keyword_score(text, keywords, weight=0.5)
    return dict(scores)


def score_episodes_center(episodes: EpisodeInput) -> dict[str, float]:
    combined = " ".join(
        [episodes.recent_conflict, episodes.core_values, episodes.emotion_handling]
    )
    return score_episode_text_for_center(combined)


def score_episode_samples_center(samples: list[EpisodeSample]) -> dict[str, float]:
    combined = " ".join(
        f"{s['event']} {s['feeling']} {s['action']}" for s in samples
    )
    return score_episode_text_for_center(combined)


def score_behavior_log_center(log: BehaviorLog) -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)

    if 0 <= log.work_role < len(_BEHAVIOR_WORK_CENTER):
        scores[_BEHAVIOR_WORK_CENTER[log.work_role].value] += 1.5

    if 0 <= log.relationship_tendency < len(_BEHAVIOR_RELATION_CENTER):
        scores[_BEHAVIOR_RELATION_CENTER[log.relationship_tendency].value] += 1.0

    if 0 <= log.stress_reaction < len(_BEHAVIOR_STRESS_CENTER):
        scores[_BEHAVIOR_STRESS_CENTER[log.stress_reaction].value] += 2.0

    return dict(scores)


def score_self_other_gap_center(gap: SelfOtherGap) -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)

    for trait in _SELF_OTHER_TRAITS:
        self_val = gap.self_image.get(trait, 0)
        other_val = gap.others_image.get(trait, 0)
        avg = (self_val + other_val) / 2
        for center, weight in _TRAIT_CENTER_WEIGHTS.get(trait, {}).items():
            scores[center.value] += avg * weight * 0.15

    return dict(scores)


def score_supplemental_center(data: AssessmentInput) -> dict[str, float]:
    """Aggregate supplemental signals for center refinement."""
    scores: dict[str, float] = defaultdict(float)

    for part in (
        score_episodes_center(data.episodes),
        score_episode_samples_center(data.episode_samples),
    ):
        for key, value in part.items():
            scores[key] += value

    if data.behavior_log is not None:
        for key, value in score_behavior_log_center(data.behavior_log).items():
            scores[key] += value

    if data.self_other_gap is not None:
        for key, value in score_self_other_gap_center(data.self_other_gap).items():
            scores[key] += value

    return dict(scores)


def score_episodes(episodes: EpisodeInput) -> tuple[dict[int, float], dict[str, float]]:
    """Return type score adjustments and instinct score adjustments."""
    combined = " ".join(
        [episodes.recent_conflict, episodes.core_values, episodes.emotion_handling]
    )

    type_scores: dict[int, float] = defaultdict(float)
    instinct_scores: dict[str, float] = defaultdict(float)

    for type_num, keywords in _TYPE_KEYWORDS.items():
        type_scores[type_num] += _keyword_score(combined, keywords)

    for instinct, keywords in _INSTINCT_KEYWORDS.items():
        instinct_scores[instinct] += _keyword_score(combined, keywords, weight=0.4)

    return dict(type_scores), dict(instinct_scores)


def score_behavior_log(log: BehaviorLog) -> dict[int, float]:
    """Map behavior log choices to type score adjustments."""
    type_scores: dict[int, float] = defaultdict(float)

    work_type_map = [8, 2, 5, 3, 9]
    relation_type_map = [5, 3, 5, 2, 9]

    if 0 <= log.work_role < len(work_type_map):
        type_scores[work_type_map[log.work_role]] += 1.0

    if 0 <= log.relationship_tendency < len(relation_type_map):
        type_scores[relation_type_map[log.relationship_tendency]] += 1.0

    if 0 <= log.stress_reaction <= 8:
        type_scores[log.stress_reaction + 1] += 2.0

    return dict(type_scores)


_SELF_OTHER_TRAITS: tuple[str, ...] = (
    "assertive",
    "emotional",
    "analytical",
    "helpful",
    "peaceful",
    "ambitious",
    "unique",
    "cautious",
)

_TRAIT_TYPE_WEIGHTS: dict[str, dict[int, float]] = {
    "assertive": {8: 2.0, 1: 1.0, 3: 1.0},
    "emotional": {4: 2.0, 2: 1.5, 6: 1.0},
    "analytical": {5: 2.0, 1: 1.0, 6: 1.0},
    "helpful": {2: 2.0, 9: 1.0},
    "peaceful": {9: 2.0, 2: 0.5},
    "ambitious": {3: 2.0, 8: 1.0},
    "unique": {4: 2.0, 7: 1.0},
    "cautious": {6: 2.0, 5: 1.0, 1: 0.5},
}


def score_self_other_gap(gap: SelfOtherGap) -> dict[int, float]:
    """
    Score type adjustments from self vs others perception gap.
    Large gaps on certain traits indicate hidden motivations.
    """
    type_scores: dict[int, float] = defaultdict(float)

    for trait in _SELF_OTHER_TRAITS:
        self_val = gap.self_image.get(trait, 0)
        other_val = gap.others_image.get(trait, 0)
        delta = abs(self_val - other_val)

        if delta < 2:
            continue

        for type_num, weight in _TRAIT_TYPE_WEIGHTS.get(trait, {}).items():
            type_scores[type_num] += delta * weight * 0.2

    return dict(type_scores)


def merge_type_scores(*score_dicts: dict[int, float]) -> dict[int, float]:
    merged: dict[int, float] = defaultdict(float)
    for scores in score_dicts:
        for type_num, value in scores.items():
            merged[type_num] += value
    return dict(merged)


def normalize_type_scores(scores: dict[int, float]) -> dict[int, float]:
    if not scores:
        return {n: 0.0 for n in range(1, 10)}
    total = sum(scores.values()) or 1.0
    return {n: scores.get(n, 0.0) / total for n in range(1, 10)}


def apply_center_filter(scores: dict[int, float], center: Center) -> dict[int, float]:
    allowed = set(CENTER_TYPES[center])
    return {n: v for n, v in scores.items() if n in allowed}


def merge_type_scores_weighted(
    question_totals: dict[int, float],
    supplemental: dict[int, float],
    center: Center,
) -> dict[int, float]:
    """Blend question-based and supplemental type scores (70% / 30%)."""
    center_types = CENTER_TYPES[center]
    q_filtered = {t: question_totals.get(t, 0.0) for t in center_types}
    s_filtered = apply_center_filter(supplemental, center)
    s_sum = sum(s_filtered.values())
    if s_sum <= 0:
        return q_filtered

    q_sum = sum(q_filtered.values()) or 1.0
    scale = q_sum / s_sum
    merged: dict[int, float] = {}
    for t in center_types:
        merged[t] = (
            q_filtered.get(t, 0.0) * TYPE_QUESTION_WEIGHT
            + s_filtered.get(t, 0.0) * scale * TYPE_SUPPLEMENTAL_WEIGHT
        )
    return merged


@dataclass(frozen=True)
class RefinedTypeResult:
    refined: int
    question_primary: int
    question_totals: dict[int, float]
    question_confidence: float
    merged_totals: dict[int, float]
    confidence: float
    adjusted: bool
    borderline: bool = False


def refine_type_from_supplemental_only(
    center: Center,
    supplemental: dict[int, float],
) -> RefinedTypeResult:
    """Estimate primary type from supplemental data when Step 2 answers do not apply."""
    types_in = CENTER_TYPES[center]
    merged = {t: supplemental.get(t, 0.0) for t in types_in}
    total = sum(merged.values()) or 1.0
    refined = max(types_in, key=lambda t: merged.get(t, 0.0))
    confidence = merged.get(refined, 0.0) / total if total > 0 else 0.0
    return RefinedTypeResult(
        refined=refined,
        question_primary=refined,
        question_totals={t: 0.0 for t in types_in},
        question_confidence=0.0,
        merged_totals=merged,
        confidence=confidence,
        adjusted=False,
        borderline=True,
    )


def gather_supplemental_type(data: AssessmentInput) -> dict[int, float]:
    """Collect supplemental type scores from assessment input."""
    supplemental_type: dict[int, float] = defaultdict(float)

    episode_type, _ = score_episodes(data.episodes)
    supplemental_type = merge_type_scores(supplemental_type, episode_type)

    if data.behavior_log is not None:
        supplemental_type = merge_type_scores(
            supplemental_type, score_behavior_log(data.behavior_log)
        )

    if data.self_other_gap is not None:
        supplemental_type = merge_type_scores(
            supplemental_type, score_self_other_gap(data.self_other_gap)
        )

    return dict(supplemental_type)


def refine_primary_type_detailed(
    center: Center,
    type_answers: dict[str, int],
    supplemental: dict[int, float],
    type_tiebreak_answers: dict[str, int] | None = None,
    type_tiebreak_pair: tuple[int, int] | None = None,
) -> RefinedTypeResult:
    """Combine Step 2 type answers with supplemental data (70% / 30%)."""
    center_types = CENTER_TYPES[center]
    question_totals = score_type_totals_in_center(
        center,
        type_answers,
        type_tiebreak_answers,
        type_tiebreak_pair,
    )
    if not question_totals:
        question_primary = center_types[0]
    else:
        question_primary = max(question_totals, key=question_totals.get)

    q_total = sum(question_totals.values()) or 1.0
    question_confidence = question_totals.get(question_primary, 0.0) / q_total
    type_base = analyze_type_base(center, type_answers)

    merged = merge_type_scores_weighted(question_totals, supplemental, center)
    if not merged:
        refined = question_primary
    else:
        refined = max(center_types, key=lambda t: merged.get(t, 0.0))

    total = sum(merged.values()) or 1.0
    confidence = merged.get(refined, 0.0) / total
    adjusted = refined != question_primary

    return RefinedTypeResult(
        refined=refined,
        question_primary=question_primary,
        question_totals=dict(question_totals),
        question_confidence=question_confidence,
        merged_totals=merged,
        confidence=confidence,
        adjusted=adjusted,
        borderline=type_base.borderline,
    )


def refine_primary_type(
    center: Center,
    type_answers: dict[str, int],
    supplemental: dict[int, float],
) -> int:
    """Combine question-based type with supplemental signals."""
    return refine_primary_type_detailed(center, type_answers, supplemental).refined
