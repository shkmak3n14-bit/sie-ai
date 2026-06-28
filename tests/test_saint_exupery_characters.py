"""Tests for Saint-Exupéry character model (Type 3 / 4 separation)."""

from sie.enneagram.context import get_enneagram_instruction
from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.report import format_report_plain
from sie.enneagram.saint_exupery_characters import (
    CHARACTER_ARCHETYPES,
    get_saint_exupery_characters,
)
from sie.flow import ConversationPhase
from sie.session import Session


def _profile(primary: int, wing: int) -> EnneagramProfile:
    return EnneagramProfile(
        primary_type=primary,
        wing=wing,
        scores={n: 0.1 for n in range(1, 10)},
        summary="テスト",
        strengths=["分析力"],
        blind_spots=["孤立"],
        stress_pattern=7,
        growth_pattern=1,
        instinctual_variant="sp",
        core_fear="無能",
        core_desire="有能",
        communication_style="簡潔",
        conflict_pattern="距離",
        relationship_needs=["時間"],
        childhood_wound="—",
        episode_samples=[],
    )


def test_four_characters_defined() -> None:
    assert set(CHARACTER_ARCHETYPES) == {"prince", "rose", "fox", "pilot"}


def test_4w3_gets_all_four_characters() -> None:
    chars = get_saint_exupery_characters(4, 3)
    names = [c.name for c in chars]
    assert names == ["王子さま", "バラ", "キツネ", "飛行士"]


def test_3w4_gets_pilot_prince_fox() -> None:
    chars = get_saint_exupery_characters(3, 4)
    names = [c.name for c in chars]
    assert names == ["飛行士", "王子さま", "キツネ"]


def test_4w5_excludes_pilot() -> None:
    chars = get_saint_exupery_characters(4, 5)
    names = [c.name for c in chars]
    assert "飛行士" not in names
    assert "王子さま" in names


def test_type_5_gets_no_characters() -> None:
    assert get_saint_exupery_characters(5, 4) == ()


def test_4w3_instruction_includes_character_model() -> None:
    session = Session.create()
    session.enneagram = _profile(4, 3)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "星の王子さま模型" in instruction
    assert "王子さま" in instruction
    assert "飛行士" in instruction
    assert "内面の4と外面の3" in instruction


def test_3w4_report_includes_pilot() -> None:
    report = format_report_plain(_profile(3, 4))
    assert "星の王子さま模型" in report
    assert "飛行士" in report
    assert "社会的仮面" in report
