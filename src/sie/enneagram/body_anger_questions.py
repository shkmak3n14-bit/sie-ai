"""Mandatory anger-pattern questions for body center (8 vs 9, 8w7 vs 8w9).

Three dimensions (must be in scoring logic):
  1. Ignition timing — immediate vs delayed (9→8 pattern → type 8 / wing 9)
  2. Fire persistence — explosion vs quiet burn (9 persistence × 8 resolve → wing 9)
  3. Action timing — immediate vs next opportunity (9 suppression → 8 action → type 8 / wing 9)
"""

from __future__ import annotations

from collections import defaultdict

from sie.enneagram.questions import Question, _opts

BODY_ANGER_OPTION_WEIGHT = 3.0

BODY_ANGER_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="ba_01",
        text="理不尽なことを言われたとき、怒りの「点火」に近いのは？",
        category="anger_pattern",
        options=_opts(
            ("その場ですぐ火がつく", {"8": BODY_ANGER_OPTION_WEIGHT}),
            (
                "最初は我慢するが、あとから火がつく",
                {"8": BODY_ANGER_OPTION_WEIGHT},
            ),
            (
                "火がつきにくく、距離を取って穏やかに過ごす",
                {"9": BODY_ANGER_OPTION_WEIGHT},
            ),
        ),
    ),
    Question(
        id="ba_02",
        text="イライラや怒りの「持続の仕方」に近いのは？",
        category="anger_pattern",
        options=_opts(
            ("爆発的に一気に出る", {"8": BODY_ANGER_OPTION_WEIGHT}),
            (
                "静かに燃え続け、決意が固まってから動く",
                {"8": BODY_ANGER_OPTION_WEIGHT},
            ),
            ("すぐ消して、距離を取って忘れる", {"9": BODY_ANGER_OPTION_WEIGHT}),
        ),
    ),
    Question(
        id="ba_03",
        text="怒りや不満が残ったとき、「行動のタイミング」に近いのは？",
        category="anger_pattern",
        options=_opts(
            ("その場ですぐ行動する", {"8": BODY_ANGER_OPTION_WEIGHT}),
            (
                "次の機会にはっきり行動する（その場では我慢）",
                {"8": BODY_ANGER_OPTION_WEIGHT},
            ),
            ("行動せず、我慢して関係を保つ", {"9": BODY_ANGER_OPTION_WEIGHT}),
        ),
    ),
)

# Per option index: wing 7 (8w7) or wing 9 (8w9); None = no wing signal (type 9 pattern).
BODY_ANGER_WING_BY_OPTION: dict[str, tuple[tuple[int, float] | None, ...]] = {
    "ba_01": (
        (7, BODY_ANGER_OPTION_WEIGHT),
        (9, BODY_ANGER_OPTION_WEIGHT),
        None,
    ),
    "ba_02": (
        (7, BODY_ANGER_OPTION_WEIGHT),
        (9, BODY_ANGER_OPTION_WEIGHT),
        None,
    ),
    "ba_03": (
        (7, BODY_ANGER_OPTION_WEIGHT),
        (9, BODY_ANGER_OPTION_WEIGHT),
        None,
    ),
}


def score_body_anger_for_wing(type_answers: dict[str, int]) -> dict[int, float]:
    """Apply mandatory anger-pattern answers to wing 7 vs 9 when primary is 8."""
    totals: dict[int, float] = defaultdict(float)
    for qid, wing_per_option in BODY_ANGER_WING_BY_OPTION.items():
        idx = type_answers.get(qid)
        if idx is None or idx < 0 or idx >= len(wing_per_option):
            continue
        mapping = wing_per_option[idx]
        if mapping:
            wing, weight = mapping
            totals[wing] += weight
    return dict(totals)


def get_body_anger_type_questions() -> tuple[Question, ...]:
    return BODY_ANGER_TYPE_QUESTIONS
