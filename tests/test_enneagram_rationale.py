"""Tests for assessment rationale explanations."""

from sie.enneagram.center_crosscheck import CrossCenterAnalysis
from sie.enneagram.rationale import build_reasoning
from sie.enneagram.types import Center


def _aligned_cross() -> CrossCenterAnalysis:
    return CrossCenterAnalysis(
        alignment_by_center={
            Center.BODY: 14.0,
            Center.HEART: 4.0,
            Center.HEAD: 2.0,
        },
        best_type_by_center={Center.BODY: 8, Center.HEART: 2, Center.HEAD: 5},
        best_center=Center.BODY,
        selected_center=Center.BODY,
        type_answered_center=Center.BODY,
        mismatch=False,
        margin_ratio=0.0,
    )


def test_rationale_explains_wing_vs_type_score() -> None:
    reasoning = build_reasoning(
        center=Center.BODY,
        center_totals={"body": 20.0, "heart": 5.0, "head": 3.0},
        center_confidence=0.71,
        center_tiebreak_used=False,
        center_tiebreak_pair=None,
        center_adjusted_by_supplemental=False,
        center_supplemental_totals={"body": 1.5},
        center_supplemental_suggested=None,
        question_center=Center.BODY,
        cross_center=_aligned_cross(),
        cross_center_adjusted=False,
        type_answered_center=Center.BODY,
        center_changed_for_type=False,
        type_reconfirmed=False,
        type_supplemental_only=False,
        type_tiebreak_used=False,
        type_tiebreak_pair=None,
        type_reconfirm_tiebreak_used=False,
        type_reconfirm_tiebreak_pair=None,
        question_primary=8,
        refined_primary=8,
        type_confidence=0.75,
        type_question_confidence=0.68,
        type_question_totals={8: 12.0, 9: 4.0, 1: 2.0},
        type_adjusted_by_supplemental=False,
        type_totals_in_center={8: 12.0, 9: 4.0, 1: 2.0},
        supplemental_type={8: 1.0},
        wing=7,
        wing_low=7,
        wing_high=9,
        wing_totals={"wing_low": 4.0, "wing_high": 2.0},
        instinct_variant="sp",
        instinct_totals={"sp": 10.0, "so": 3.0, "sx": 2.0},
        normalized_scores={t: (0.54 if t == 8 else (0.09 if t == 9 else 0.0)) for t in range(1, 10)},
    )

    text = "\n".join(reasoning)
    assert "8w7" in text or ("ウイング 7" in text and "タイプ 8" in text)
    assert "タイプ7が低くても w7" in text
    assert "クロス検証" in text
    assert "参考" in text
    assert "質問のみの信頼度" in text


def test_rationale_center_changed_type_warning() -> None:
    reasoning = build_reasoning(
        center=Center.HEART,
        center_totals={"body": 18.0, "heart": 22.0, "head": 5.0},
        center_confidence=0.62,
        center_tiebreak_used=False,
        center_tiebreak_pair=None,
        center_adjusted_by_supplemental=True,
        center_supplemental_totals={"heart": 10.0},
        center_supplemental_suggested=None,
        question_center=Center.BODY,
        cross_center=_aligned_cross(),
        cross_center_adjusted=False,
        type_answered_center=Center.BODY,
        center_changed_for_type=True,
        type_reconfirmed=True,
        type_supplemental_only=False,
        type_tiebreak_used=False,
        type_tiebreak_pair=None,
        type_reconfirm_tiebreak_used=False,
        type_reconfirm_tiebreak_pair=None,
        question_primary=2,
        refined_primary=2,
        type_confidence=0.72,
        type_question_confidence=0.65,
        type_question_totals={2: 10.0, 3: 4.0, 4: 2.0},
        type_adjusted_by_supplemental=False,
        type_totals_in_center={2: 10.0, 3: 4.0, 4: 2.0},
        supplemental_type={2: 1.0},
        wing=3,
        wing_low=1,
        wing_high=3,
        wing_totals={"wing_low": 2.0, "wing_high": 5.0},
        instinct_variant="so",
        instinct_totals={"sp": 3.0, "so": 8.0, "sx": 2.0},
        normalized_scores={t: 0.11 for t in range(1, 10)},
    )
    text = "\n".join(reasoning)
    assert "センター変更" in text
    assert "タイプ再確認" in text
