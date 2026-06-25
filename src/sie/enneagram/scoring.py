"""Scoring logic for the Enneagram assessment."""

from __future__ import annotations

from collections import defaultdict

from sie.enneagram.inputs import AssessmentInput, BehaviorLog, EpisodeInput, SelfOtherGap
from sie.enneagram.profile import InstinctualVariant
from sie.enneagram.questions import (
    CENTER_QUESTIONS,
    CENTER_TYPE_QUESTIONS,
    INSTINCT_QUESTIONS,
    Question,
)
from sie.enneagram.wing_questions import get_wing_questions
from sie.enneagram.types import CENTER_TYPES, Center, wing_types


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


def score_center(answers: dict[str, int]) -> Center:
    totals = score_center_totals(answers)
    winner = _winner(totals)
    return Center(winner)


def score_center_totals(answers: dict[str, int]) -> dict[str, float]:
    return _score_from_answers(CENTER_QUESTIONS, answers, ("body", "heart", "head"))


def score_type_totals_in_center(center: Center, answers: dict[str, int]) -> dict[int, float]:
    questions = CENTER_TYPE_QUESTIONS[center]
    type_keys = tuple(str(t) for t in CENTER_TYPES[center])
    totals = _score_from_answers(questions, answers, type_keys)
    return {int(k): v for k, v in totals.items()}


def score_type_in_center(center: Center, answers: dict[str, int]) -> int:
    totals = score_type_totals_in_center(center, answers)
    if not totals:
        raise ValueError("スコアが空です。回答を確認してください。")
    return max(totals, key=totals.get)


def score_wing_detail(
    primary_type: int,
    answers: dict[str, int],
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
    if not totals_raw:
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
    Center.BODY: ("怒り", "体", "即座", "正しい", "平和", "硬い"),
    Center.HEART: ("評価", "愛", "必要", "感情", "承認", "意味"),
    Center.HEAD: ("不安", "分析", "可能性", "リスク", "考える", "情報"),
}

_INSTINCT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "sp": ("お金", "健康", "安全", "備え", "生活", "住居", "節約"),
    "so": ("所属", "役割", "評価", "グループ", "立場", "ネットワーク"),
    "sx": ("親密", "一人", "情熱", "深い", "特別", "関係"),
}


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


def refine_primary_type(
    center: Center,
    question_primary: int,
    supplemental: dict[int, float],
) -> int:
    """Combine question-based type with supplemental signals."""
    center_types = CENTER_TYPES[center]
    combined = merge_type_scores(
        {question_primary: 5.0},
        apply_center_filter(supplemental, center),
    )

    best = max(center_types, key=lambda t: combined.get(t, 0.0))
    return best
