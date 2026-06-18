"""Session state management for S.I.E."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sie.flow import ConversationPhase
from sie.humor import schedule_next_humor

if TYPE_CHECKING:
    from sie.enneagram.profile import EnneagramProfile


@dataclass
class Session:
    user_name: str = "あなた"
    phase: ConversationPhase = ConversationPhase.GREETING
    turn_count: int = 0
    messages: list[dict[str, str]] = field(default_factory=list)
    humor_next_at: int = 7
    awaiting_casual_name: bool = False
    greeted: bool = False
    enneagram: EnneagramProfile | None = None

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def increment_turn(self) -> None:
        self.turn_count += 1

    @classmethod
    def create(cls) -> Session:
        session = cls()
        session.humor_next_at = schedule_next_humor(0)
        return session
