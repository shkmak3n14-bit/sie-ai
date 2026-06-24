"""Streamlit web UI for S.I.E."""

from __future__ import annotations

import streamlit as st

from sie.enneagram.ui import render_enneagram_assessment
from sie.enneagram.types import get_type_info
from sie.episode import RELATIONSHIP_ROLES, RelationshipEpisode, format_episode_user_message
from sie.flow import ConversationPhase, is_closing_request
from sie.llm import generate_closing, generate_episode_analysis, generate_greeting, generate_reply
from sie.session import Session
from sie.styles import APP_CSS

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
    _sync_enneagram_to_session()


def _sync_enneagram_to_session() -> None:
    """Attach Enneagram profile from UI state to the active S.I.E. session."""
    if "sie_session" not in st.session_state:
        return
    st.session_state.sie_session.enneagram = st.session_state.get("enneagram_profile")


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


def _handle_episode_submit(episode: RelationshipEpisode) -> None:
    user_message = format_episode_user_message(episode)
    st.session_state.display_messages.append(
        {"role": "user", "content": user_message}
    )

    session: Session = st.session_state.sie_session

    try:
        with st.spinner("サイがエピソードを分析しています…"):
            reply = generate_episode_analysis(session, episode, user_message)
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


def _render_episode_form() -> None:
    with st.expander("エピソードを共有する", expanded=False):
        st.caption(
            "人間関係の出来事を入力すると、サイが6つの観点から分析します。"
        )

        col1, col2 = st.columns(2)
        with col1:
            subject_name = st.text_input(
                "1. ○○さんが",
                placeholder="名前（例：太郎）",
                key="episode_subject_name",
            )
            subject_role = st.selectbox(
                "　関係（主語）",
                RELATIONSHIP_ROLES,
                key="episode_subject_role",
            )
        with col2:
            target_name = st.text_input(
                "2. ○○さんに",
                placeholder="名前（例：花子）",
                key="episode_target_name",
            )
            target_role = st.selectbox(
                "　関係（対象）",
                RELATIONSHIP_ROLES,
                key="episode_target_role",
            )

        action = st.text_area(
            "3. 何を言った / 何をした",
            placeholder="例：突然厳しい口調で注意した",
            height=80,
            key="episode_action",
        )
        user_reaction = st.text_area(
            "4. あなたはどう思ったか / どのような行動をしたか",
            placeholder="例：傷ついたが、黙って受け止めた",
            height=80,
            key="episode_user_reaction",
        )

        if st.button("サイに分析してもらう", use_container_width=True, type="primary"):
            if not subject_name.strip():
                st.error("1. の名前を入力してください。")
            elif not target_name.strip():
                st.error("2. の名前を入力してください。")
            elif not action.strip():
                st.error("3. を入力してください。")
            elif not user_reaction.strip():
                st.error("4. を入力してください。")
            else:
                episode = RelationshipEpisode(
                    subject_name=subject_name.strip(),
                    subject_role=subject_role,
                    target_name=target_name.strip(),
                    target_role=target_role,
                    action=action.strip(),
                    user_reaction=user_reaction.strip(),
                )
                _handle_episode_submit(episode)
                st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="S.I.E.（サイ）",
        page_icon="🧩",
        layout="centered",
    )

    st.markdown(APP_CSS, unsafe_allow_html=True)

    if "sie_session" not in st.session_state:
        _init_session()
    else:
        _sync_enneagram_to_session()

    if "app_mode" not in st.session_state:
        st.session_state.app_mode = "会話"

    if st.session_state.pop("full_initialize_requested", False):
        _reset_session()
        st.session_state.app_mode = "会話"

    with st.sidebar:
        st.markdown("### S.I.E.（サイ）")
        st.markdown(
            '<p class="sie-caption">Support Intelligence on Ego</p>',
            unsafe_allow_html=True,
        )
        st.divider()

        st.session_state.app_mode = st.radio(
            "画面",
            ["会話", "エニアグラム診断"],
            index=0 if st.session_state.app_mode == "会話" else 1,
        )

        if st.session_state.get("enneagram_profile"):
            profile = st.session_state.enneagram_profile
            type_info = get_type_info(profile.primary_type)
            st.divider()
            st.markdown("**診断結果**")
            st.caption(type_info.name)
            if profile.wing:
                st.caption(f"ウイング: {profile.wing}")

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

    if st.session_state.app_mode == "エニアグラム診断":
        render_enneagram_assessment()
        return

    st.title("S.I.E.（サイ）")
    st.caption("落ち着いた声で、核心を静かに伝える")

    _ensure_greeting()
    _render_chat()

    if st.session_state.session_ended:
        st.info("セッションは終了しました。サイドバーから新しいセッションを始められます。")
        return

    _render_episode_form()

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
