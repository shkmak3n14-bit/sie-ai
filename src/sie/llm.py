"""OpenAI LLM integration for S.I.E."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

from sie.enneagram.context import get_enneagram_instruction
from sie.episode import RelationshipEpisode, get_episode_analysis_instruction
from sie.flow import advance_phase, get_name_response_hint, get_phase_instruction, GREETING_TEXT
from sie.humor import get_humor_instruction
from sie.personality import SYSTEM_PROMPT
from sie.session import Session

load_dotenv()

DEFAULT_MODEL = "gpt-4o"
TEMPERATURE = 0.7


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY が設定されていません。.env ファイルを確認してください。"
        )
    return OpenAI(api_key=api_key)


def _get_model() -> str:
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def _build_user_message(user_input: str, instructions: list[str]) -> str:
    if not instructions:
        return user_input
    meta = "\n".join(f"- {item}" for item in instructions)
    return f"{user_input}\n\n[内部指示:\n{meta}]"


def generate_reply(session: Session, user_input: str) -> str:
    """Generate S.I.E. response for the given user input."""
    phase_instruction = get_phase_instruction(session)
    name_hint = get_name_response_hint(session, user_input)

    advance_phase(session, user_input)

    instructions: list[str] = [phase_instruction]
    if name_hint:
        instructions.append(name_hint)

    humor_instruction = get_humor_instruction(session)
    if humor_instruction:
        instructions.append(humor_instruction)

    enneagram_instruction = get_enneagram_instruction(session)
    if enneagram_instruction:
        instructions.append(enneagram_instruction)

    if user_input.strip():
        session.add_user_message(user_input.strip())

    client = _get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *session.messages]

    if user_input.strip():
        messages[-1] = {
            "role": "user",
            "content": _build_user_message(user_input.strip(), instructions),
        }
    else:
        messages.append({
            "role": "user",
            "content": _build_user_message("", instructions),
        })

    response = client.chat.completions.create(
        model=_get_model(),
        messages=messages,
        temperature=TEMPERATURE,
    )

    reply = response.choices[0].message.content or ""
    session.add_assistant_message(reply)
    session.increment_turn()
    return reply


def generate_episode_analysis(
    session: Session,
    episode: RelationshipEpisode,
    user_message: str,
) -> str:
    """Generate S.I.E. analysis for a shared relationship episode."""
    from sie.flow import ConversationPhase

    if session.phase == ConversationPhase.NAME_CONFIRM:
        session.phase = ConversationPhase.EMPATHY

    instructions: list[str] = [
        get_episode_analysis_instruction(episode),
        "通常の会話フローより、エピソード分析を優先してください。",
    ]

    enneagram_instruction = get_enneagram_instruction(session)
    if enneagram_instruction:
        instructions.append(enneagram_instruction)

    session.add_user_message(user_message)

    client = _get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *session.messages[:-1]]
    messages.append({
        "role": "user",
        "content": _build_user_message(user_message, instructions),
    })

    response = client.chat.completions.create(
        model=_get_model(),
        messages=messages,
        temperature=TEMPERATURE,
    )

    reply = response.choices[0].message.content or ""
    session.add_assistant_message(reply)
    session.increment_turn()
    if session.phase == ConversationPhase.EMPATHY:
        session.phase = ConversationPhase.ONGOING
    return reply


def generate_greeting(session: Session) -> str:
    """Generate initial greeting without user input."""
    from sie.flow import ConversationPhase

    reply = GREETING_TEXT
    session.add_assistant_message(reply)
    session.greeted = True
    session.phase = ConversationPhase.NAME_CONFIRM
    session.increment_turn()
    return reply


def generate_closing(session: Session) -> str:
    """Generate closing message when user exits."""
    from sie.flow import ConversationPhase

    session.phase = ConversationPhase.CLOSING
    instructions = [get_phase_instruction(session)]
    enneagram_instruction = get_enneagram_instruction(session)
    if enneagram_instruction:
        instructions.append(enneagram_instruction)

    client = _get_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *session.messages,
        {
            "role": "user",
            "content": _build_user_message("（セッション終了）", instructions),
        },
    ]

    response = client.chat.completions.create(
        model=_get_model(),
        messages=messages,
        temperature=TEMPERATURE,
    )

    reply = response.choices[0].message.content or ""
    session.add_assistant_message(reply)
    session.increment_turn()
    return reply
