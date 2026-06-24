"""Tests for S.I.E. conversation flow and humor control."""

import random

import pytest

from sie.flow import (
    ConversationPhase,
    advance_phase,
    get_name_response_hint,
    get_phase_instruction,
    is_casual_name_request,
    is_closing_request,
)
from sie.humor import get_humor_instruction, schedule_next_humor, should_use_humor
from sie.session import Session


@pytest.fixture
def session() -> Session:
    return Session.create()


def test_greeting_advances_to_name_confirm(session: Session) -> None:
    session.phase = ConversationPhase.GREETING
    advance_phase(session, "")
    assert session.phase == ConversationPhase.NAME_CONFIRM


def test_name_confirm_registers_name(session: Session) -> None:
    session.phase = ConversationPhase.NAME_CONFIRM
    advance_phase(session, "太郎")
    assert session.user_name == "太郎"
    assert session.phase == ConversationPhase.EMPATHY


def test_name_confirm_empty_defaults_to_anata(session: Session) -> None:
    session.phase = ConversationPhase.NAME_CONFIRM
    advance_phase(session, "")
    assert session.user_name == "あなた"
    assert session.phase == ConversationPhase.EMPATHY


def test_name_confirm_casual_name_request(session: Session) -> None:
    session.phase = ConversationPhase.NAME_CONFIRM
    advance_phase(session, "好きに呼んで")
    assert session.awaiting_casual_name is True
    assert session.phase == ConversationPhase.NAME_CONFIRM


def test_name_confirm_casual_then_register(session: Session) -> None:
    session.phase = ConversationPhase.NAME_CONFIRM
    advance_phase(session, "好きに呼んで")
    hint = get_name_response_hint(session, "好きに呼んで")
    assert hint is None

    advance_phase(session, "花子")
    assert session.user_name == "花子"
    assert session.phase == ConversationPhase.EMPATHY


def test_name_response_hint_for_silence(session: Session) -> None:
    session.phase = ConversationPhase.NAME_CONFIRM
    hint = get_name_response_hint(session, "")
    assert hint is not None
    assert "あなた" in hint


def test_name_response_hint_for_registration(session: Session) -> None:
    session.phase = ConversationPhase.NAME_CONFIRM
    hint = get_name_response_hint(session, "太郎")
    assert hint is not None
    assert "登録しました" in hint


def test_empathy_advances_to_core(session: Session) -> None:
    session.phase = ConversationPhase.EMPATHY
    advance_phase(session, "最近仕事がつらいです")
    assert session.phase == ConversationPhase.CORE


def test_core_advances_to_guidance(session: Session) -> None:
    session.phase = ConversationPhase.CORE
    advance_phase(session, "なるほど")
    assert session.phase == ConversationPhase.GUIDANCE


def test_guidance_advances_to_closing(session: Session) -> None:
    session.phase = ConversationPhase.GUIDANCE
    advance_phase(session, "考えてみます")
    assert session.phase == ConversationPhase.CLOSING


def test_closing_request_jumps_to_closing(session: Session) -> None:
    session.phase = ConversationPhase.EMPATHY
    advance_phase(session, "終了")
    assert session.phase == ConversationPhase.CLOSING


def test_full_phase_sequence(session: Session) -> None:
    session.phase = ConversationPhase.GREETING
    advance_phase(session, "")
    assert session.phase == ConversationPhase.NAME_CONFIRM

    advance_phase(session, "太郎")
    assert session.phase == ConversationPhase.EMPATHY

    advance_phase(session, "悩んでいます")
    assert session.phase == ConversationPhase.CORE

    advance_phase(session, "うん")
    assert session.phase == ConversationPhase.GUIDANCE

    advance_phase(session, "ありがとう")
    assert session.phase == ConversationPhase.CLOSING


def test_phase_instructions_contain_key_phrases(session: Session) -> None:
    session.phase = ConversationPhase.GREETING
    assert "何から始めましょうか" in get_phase_instruction(session)

    session.phase = ConversationPhase.NAME_CONFIRM
    assert "お呼びすれば" in get_phase_instruction(session)

    session.phase = ConversationPhase.EMPATHY
    assert "寄り添い" in get_phase_instruction(session)

    session.phase = ConversationPhase.CORE
    assert "核心" in get_phase_instruction(session)

    session.phase = ConversationPhase.GUIDANCE
    assert "相手" in get_phase_instruction(session)

    session.phase = ConversationPhase.CLOSING
    assert "1mm" in get_phase_instruction(session)


def test_humor_schedule_interval(session: Session) -> None:
    random.seed(42)
    next_at = schedule_next_humor(0)
    assert 7 <= next_at <= 8


def test_humor_triggers_at_scheduled_turn(session: Session) -> None:
    session.humor_next_at = 3
    session.turn_count = 2
    assert should_use_humor(session) is False

    session.turn_count = 3
    assert should_use_humor(session) is True


def test_humor_instruction_reschedules(session: Session) -> None:
    random.seed(0)
    session.humor_next_at = 1
    session.turn_count = 1

    instruction = get_humor_instruction(session)
    assert instruction is not None
    assert "ユーモア" in instruction
    assert session.humor_next_at > session.turn_count


def test_is_casual_name_request() -> None:
    assert is_casual_name_request("好きに呼んで") is True
    assert is_casual_name_request("なんでもいいよ") is True
    assert is_casual_name_request("太郎") is False


def test_is_closing_request() -> None:
    assert is_closing_request("exit") is True
    assert is_closing_request("終了します") is True
    assert is_closing_request("悩んでいます") is False
