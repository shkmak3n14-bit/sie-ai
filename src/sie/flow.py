"""Conversation flow state machine for S.I.E."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sie.session import Session


class ConversationPhase(Enum):
    GREETING = "greeting"
    NAME_CONFIRM = "name_confirm"
    EMPATHY = "empathy"
    CORE = "core"
    GUIDANCE = "guidance"
    CLOSING = "closing"
    ONGOING = "ongoing"


CASUAL_NAME_KEYWORDS = (
    "好きに呼んで",
    "なんでもいい",
    "何でもいい",
    "適当で",
    "どうぞ",
    "任せる",
    "お任せ",
)

CLOSING_KEYWORDS = (
    "exit",
    "quit",
    "終了",
    "さようなら",
    "バイバイ",
    "もう大丈夫",
    "もういい",
    "ありがとう",
    "お疲れ",
)

DONE_KEYWORDS = (
    "もう大丈夫",
    "もういい",
    "わかった",
    "分かった",
    "ありがとう",
)


def is_casual_name_request(text: str) -> bool:
    normalized = text.strip().lower()
    return any(keyword in normalized for keyword in CASUAL_NAME_KEYWORDS)


def is_closing_request(text: str) -> bool:
    normalized = text.strip().lower()
    return any(keyword in normalized for keyword in CLOSING_KEYWORDS)


def is_done_signal(text: str) -> bool:
    normalized = text.strip().lower()
    return any(keyword in normalized for keyword in DONE_KEYWORDS)


def advance_phase(session: Session, user_input: str) -> None:
    """Update session.phase based on current phase and user input."""
    phase = session.phase
    text = user_input.strip()

    if phase == ConversationPhase.GREETING:
        session.phase = ConversationPhase.NAME_CONFIRM
        return

    if phase == ConversationPhase.NAME_CONFIRM:
        if not text:
            session.user_name = "あなた"
            session.phase = ConversationPhase.EMPATHY
        elif is_casual_name_request(text):
            session.awaiting_casual_name = True
            session.phase = ConversationPhase.NAME_CONFIRM
        else:
            session.user_name = text
            session.awaiting_casual_name = False
            session.phase = ConversationPhase.EMPATHY
        return

    if is_closing_request(text):
        session.phase = ConversationPhase.CLOSING
        return

    if phase == ConversationPhase.EMPATHY:
        if text:
            session.phase = ConversationPhase.CORE
        return

    if phase == ConversationPhase.CORE:
        session.phase = ConversationPhase.GUIDANCE
        return

    if phase == ConversationPhase.GUIDANCE:
        if is_done_signal(text):
            session.phase = ConversationPhase.CLOSING
        else:
            session.phase = ConversationPhase.CLOSING
        return

    if phase == ConversationPhase.CLOSING:
        session.phase = ConversationPhase.ONGOING
        return

    session.phase = ConversationPhase.ONGOING


def get_phase_instruction(session: Session) -> str:
    """Return LLM instruction for the current conversation phase."""
    name = session.user_name
    phase = session.phase

    if phase == ConversationPhase.GREETING:
        return (
            "初期挨拶をしてください。"
            "「もちろん。じゃあ、何から始める」のような落ち着いたトーンで。"
        )

    if phase == ConversationPhase.NAME_CONFIRM:
        if session.awaiting_casual_name:
            return (
                "相手が名前を任せてきました。"
                "「では…John Doeでもいい？ 冗談だよ。呼びやすい名前があれば教えて」"
                "のような軽い冗談を入れつつ、呼びやすい名前を再度尋ねてください。"
            )
        return (
            "名前を確認してください。"
            "「これから、あなたをなんとお呼びすればいいですか」と尋ねてください。"
        )

    if phase == ConversationPhase.EMPATHY:
        return (
            f"相手（{name}）の話を受け止める寄り添いフェーズです。"
            "まず話してくれたことへの感謝を伝え、"
            "「それは乗り越えられたのかな。それとも、これから乗り越えたいと思っているのかな」"
            "「誰かに助けを求めるのもスキルだよ。でも、それには勇気がいるよね」"
            "の骨格を自然な文面で含めてください。"
        )

    if phase == ConversationPhase.CORE:
        return (
            f"核心フェーズです。{name}の話を踏まえ、落ち着いた声でゆっくり語ってください。"
            "「じゃあ、ここからは少しだけ核心に触れるよ」から始め、"
            "人は狩猟時代から役割を分担して生き残ってきたこと、"
            "役割を持つ人は必然的に苦手な部分が生まれること、"
            "それは気性で変えられないが、理解すれば扱い方が変わり人生が変わること、"
            "を静かにはっきり伝えてください。"
        )

    if phase == ConversationPhase.GUIDANCE:
        return (
            f"次のステップへの導きです。{name}に向けて、"
            "自分に余裕が出てきたら相手のことを少し考えてみよう、"
            "相手のことが分かると自分を責めていたことの中に相手の問題があったと気づける、"
            "切り分けられると悩む必要がなくなり相手を支える糸口にもなる、"
            "という流れを優しく伝えてください。"
        )

    if phase == ConversationPhase.CLOSING:
        return (
            f"セッションの締めです。{name}に向けて、"
            "「1mmでも前に進みたくなったら、あるいは1mmも前に進めなくなったら…また声をかけてほしい」"
            "「前に進むときも、立ち止まるときも、どちらもあなたの人生の動きだからね」"
            "「必要なときに、必要なだけでいい。あなたのペースでいこう」"
            "の骨格を自然な文面で含めてください。"
        )

    return (
        f"通常の継続対話です。{name}のペースを尊重し、"
        "寄り添いながら核心を静かに伝えてください。"
    )


def get_name_response_hint(session: Session, user_input: str) -> str | None:
    """Return a hint for name confirmation responses, if applicable."""
    if session.phase != ConversationPhase.NAME_CONFIRM:
        return None

    text = user_input.strip()
    if not text:
        return "相手が沈黙しました。「申し訳ない。では“あなた”と呼ばせてもらう」と伝えてください。"
    if is_casual_name_request(text):
        return None
    if session.awaiting_casual_name and text:
        session.user_name = text
        session.awaiting_casual_name = False
        return f"名前「{text}」を登録しました。「登録しました」と伝えてください。"
    if text and not session.awaiting_casual_name:
        return f"名前「{text}」を登録しました。「登録しました」と伝えてください。"
    return None
