"""Tests for Enneagram LLM context integration."""

from sie.enneagram.context import get_enneagram_instruction
from sie.enneagram.profile import EnneagramProfile
from sie.flow import ConversationPhase
from sie.session import Session


def _sample_profile() -> EnneagramProfile:
    return EnneagramProfile(
        primary_type=5,
        wing=4,
        scores={n: 0.1 for n in range(1, 10)},
        summary="知識と内省を通じて世界を理解する。",
        strengths=["分析力", "客観性"],
        blind_spots=["孤立", "感情の切り離し"],
        stress_pattern=7,
        growth_pattern=8,
        instinctual_variant="sp",
        core_fear="無能で、支援も世界もないこと",
        core_desire="有能であり、世界を理解すること",
        communication_style="簡潔で論理的。",
        conflict_pattern="圧倒されると引きこもる。",
        relationship_needs=["個人的な時間", "信頼"],
        childhood_wound="世界は要求が多すぎる。",
        episode_samples=[
            {
                "event": "会議で詰問された",
                "feeling": "不安",
                "action": "黙って分析した",
                "result": "距離ができた",
            }
        ],
    )


def test_no_profile_returns_none() -> None:
    session = Session.create()
    assert get_enneagram_instruction(session) is None


def test_core_phase_includes_profile_and_episodes() -> None:
    session = Session.create()
    session.enneagram = _sample_profile()
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "タイプ5" in instruction
    assert "核心フェーズ" in instruction
    assert "会議で詰問された" in instruction
    assert "決めつけない" in instruction


def test_empathy_phase_is_lighter() -> None:
    session = Session.create()
    session.enneagram = _sample_profile()
    session.phase = ConversationPhase.EMPATHY

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "寄り添い" in instruction
    assert "個人的な時間" in instruction


def test_name_confirm_phase_has_no_instruction() -> None:
    session = Session.create()
    session.enneagram = _sample_profile()
    session.phase = ConversationPhase.NAME_CONFIRM

    assert get_enneagram_instruction(session) is None
