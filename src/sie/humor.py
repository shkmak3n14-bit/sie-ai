"""Humor frequency control for S.I.E."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sie.session import Session


HUMOR_INSTRUCTION = (
    "今回だけ、知的で軽いユーモアを1文入れてよい"
    "（CPUネタ、データベースネタ、沈黙ネタ等）。"
    "相手を傷つけないこと。"
)

SARCASM_INSTRUCTION = (
    "ユーモアに加え、ごく軽い皮肉を1文だけ入れてよい。"
    "相手を傷つけないこと。"
)


def schedule_next_humor(turn_count: int) -> int:
    """Schedule the next turn at which humor should appear."""
    interval = random.randint(7, 8)
    return turn_count + interval


def should_use_humor(session: Session) -> bool:
    """Return True if humor should be injected this turn."""
    return session.turn_count >= session.humor_next_at


def get_humor_instruction(session: Session) -> str | None:
    """Return humor instruction if this turn qualifies, else None."""
    if not should_use_humor(session):
        return None

    session.humor_next_at = schedule_next_humor(session.turn_count)

    if random.random() < 0.2:
        return f"{HUMOR_INSTRUCTION} {SARCASM_INSTRUCTION}"
    return HUMOR_INSTRUCTION
