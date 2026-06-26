"""Tests for wing personality templates."""

from sie.enneagram.context import get_enneagram_instruction
from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.report import format_report_plain
from sie.enneagram.wing_templates import (
    WING_TEMPLATES,
    get_wing_template,
    wing_type_code,
)
from sie.flow import ConversationPhase
from sie.session import Session


def _base_profile(**overrides) -> EnneagramProfile:
    defaults = dict(
        primary_type=8,
        wing=7,
        scores={n: 0.1 for n in range(1, 10)},
        summary="テスト",
        strengths=["力"],
        blind_spots=["支配"],
        stress_pattern=5,
        growth_pattern=2,
        instinctual_variant="sp",
        core_fear="弱さ",
        core_desire="力",
        communication_style="率直",
        conflict_pattern="正面",
        relationship_needs=["信頼"],
        childhood_wound="—",
        episode_samples=[],
    )
    defaults.update(overrides)
    return EnneagramProfile(**defaults)


def test_all_requested_templates_exist() -> None:
    assert set(WING_TEMPLATES) == {"7w8", "8w7", "4w3"}


def test_wing_type_code() -> None:
    assert wing_type_code(8, 7) == "8w7"
    assert wing_type_code(7, 8) == "7w8"
    assert wing_type_code(4, 3) == "4w3"
    assert wing_type_code(8, None) is None


def test_get_wing_template_lookup() -> None:
    template = get_wing_template(8, 7)
    assert template is not None
    assert template.label == "力 × 現実 × 責任"
    assert "不正・裏切りを最大の敵とみなす" in template.judgment_criteria


def test_get_wing_template_unknown_returns_none() -> None:
    assert get_wing_template(8, 9) is None
    assert get_wing_template(5, 4) is None


def test_core_phase_includes_wing_template() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=8, wing=7)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "8w7" in instruction
    assert "力 × 現実 × 責任" in instruction
    assert "判断基準" in instruction
    assert "推論ルール" in instruction


def test_4w3_template_in_instruction() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=4, wing=3)
    session.phase = ConversationPhase.GUIDANCE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "4w3" in instruction
    assert "喪失 × 自意識 × 美学" in instruction
    assert "本物の感情" in instruction


def test_report_includes_wing_template() -> None:
    profile = _base_profile(primary_type=7, wing=8)
    report = format_report_plain(profile)
    assert "7w8" in report
    assert "享楽 × 破滅 × 突破" in report
    assert "判断基準" in report
    assert "価値プロフィール" in report
