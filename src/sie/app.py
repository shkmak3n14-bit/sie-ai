"""Streamlit web UI for S.I.E."""

from __future__ import annotations

import streamlit as st

from sie.flow import ConversationPhase, is_closing_request
from sie.llm import generate_closing, generate_greeting, generate_reply
from sie.session import Session

EXIT_COMMANDS = {"exit", "quit", "終了", "q"}

PHASE_LABELS = {
    ConversationPhase.GREETING: "初期挨拶",
    ConversationPhase.NAME_CONFIRM: "名前確認",
    ConversationPhase.EMPATHY: "寄り添い",
    ConversationPhase.CORE: "核心",
    ConversationPhase.GUIDANCE: "導き",
    ConversationPhase.CLOSING: "締め",
    ConversationPhase.ONGOING: "継続対話",
}


def _init_session() -> None:
    st.session_state.sie_session = Session.create()
    st.session_state.display_messages: list[dict[str, str]] = []
    st.session_state.session_ended = False
    st.session_state.initialized = False


def _reset_session() -> None:
    _init_session()
    st.session_state.initialized = False


def _is_exit_command(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in EXIT_COMMANDS or is_closing_request(text)


def _ensure_greeting() -> None:
    if st.session_state.initialized:
        return

    with st.spinner("サイが応答を準備しています…"):
        try:
            greeting = generate_greeting(st.session_state.sie_session)
            st.session_state.display_messages.append(
                {"role": "assistant", "content": greeting}
            )
            st.session_state.initialized = True
        except ValueError as exc:
            st.error(str(exc))
            st.stop()
        except Exception as exc:
            st.error(f"接続エラー: {exc}")
            st.stop()


def _render_chat() -> None:
    for message in st.session_state.display_messages:
        avatar = "🧩" if message["role"] == "assistant" else "🙂"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


def _handle_user_input(user_input: str) -> None:
    st.session_state.display_messages.append(
        {"role": "user", "content": user_input}
    )

    session: Session = st.session_state.sie_session

    try:
        if _is_exit_command(user_input):
            reply = generate_closing(session)
            st.session_state.session_ended = True
        else:
            reply = generate_reply(session, user_input)
    except ValueError as exc:
        st.session_state.display_messages.pop()
        st.error(str(exc))
        return
    except Exception as exc:
        st.session_state.display_messages.pop()
        st.error(f"エラー: {exc}")
        return

    st.session_state.display_messages.append(
        {"role": "assistant", "content": reply}
    )


def main() -> None:
    st.set_page_config(
        page_title="S.I.E.（サイ）",
        page_icon="🧩",
        layout="centered",
    )

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #0f1419 0%, #1a2332 100%);
            color: #e8eef4;
        }
        .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {
            color: #e8eef4;
        }
        [data-testid="stSidebar"] {
            background-color: #151d28;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {
            color: #e8eef4;
        }
        [data-testid="stChatMessage"] {
            background-color: rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 0.5rem;
        }
        [data-testid="stChatMessageContent"] p,
        [data-testid="stChatMessageContent"] span,
        [data-testid="stChatMessageContent"] li {
            color: #f5f8fc;
        }
        [data-testid="stCaptionContainer"] p {
            color: #a8bccf;
        }
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        [data-testid="stBottom"] > div {
            background-color: #0f1419;
        }
        [data-testid="stChatInput"] {
            background-color: #ffffff;
            border-color: #cccccc;
            color: #000000;
            caret-color: #000000;
        }
        [data-testid="stChatInput"] textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
            caret-color: #000000;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: rgba(0, 0, 0, 0.45) !important;
        }
        [data-testid="stChatInput"] button {
            color: #000000;
        }
        h1 { color: #b8d4f0; font-weight: 300; }
        h3 { color: #c8dff5; }
        .sie-caption { color: #a8bccf; font-size: 0.9rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "sie_session" not in st.session_state:
        _init_session()

    with st.sidebar:
        st.markdown("### S.I.E.（サイ）")
        st.markdown(
            '<p class="sie-caption">Support Intelligence on Ego</p>',
            unsafe_allow_html=True,
        )
        st.divider()

        session: Session = st.session_state.sie_session
        st.markdown(f"**お名前:** {session.user_name}")
        st.markdown(f"**フェーズ:** {PHASE_LABELS.get(session.phase, '—')}")
        st.markdown(f"**ターン:** {session.turn_count}")

        st.divider()

        if st.button("新しいセッション", use_container_width=True):
            _reset_session()
            st.rerun()

        st.markdown(
            '<p class="sie-caption">終了: exit / quit / 終了</p>',
            unsafe_allow_html=True,
        )

    st.title("S.I.E.（サイ）")
    st.caption("落ち着いた声で、核心を静かに伝える")

    _ensure_greeting()
    _render_chat()

    if st.session_state.session_ended:
        st.info("セッションは終了しました。サイドバーから新しいセッションを始められます。")
        return

    session = st.session_state.sie_session
    placeholder = "なんとお呼びすればいいですか？"
    if session.phase == ConversationPhase.EMPATHY:
        placeholder = "話してみてください…"
    elif session.phase not in (
        ConversationPhase.GREETING,
        ConversationPhase.NAME_CONFIRM,
    ):
        placeholder = "メッセージを入力…"

    if session.phase == ConversationPhase.NAME_CONFIRM:
        if st.button("名前をスキップ（「あなた」と呼ぶ）", use_container_width=True):
            _handle_user_input("")
            st.rerun()

    if prompt := st.chat_input(placeholder):
        _handle_user_input(prompt)
        st.rerun()


def run() -> None:
    """Launch the Streamlit server."""
    import sys
    from pathlib import Path

    from streamlit.web import cli as stcli

    app_path = Path(__file__).resolve()
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
