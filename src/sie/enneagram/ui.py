"""Streamlit UI for the Enneagram assessment."""

from __future__ import annotations

import streamlit as st

from sie.enneagram.assess import run_assessment
from sie.enneagram.inputs import AssessmentInput, BehaviorLog, EpisodeInput, SelfOtherGap
from sie.enneagram.profile import EpisodeSample
from sie.enneagram.questions import (
    CENTER_QUESTIONS,
    INSTINCT_QUESTIONS,
    RELATIONSHIP_OPTIONS,
    STRESS_REACTION_OPTIONS,
    WING_QUESTIONS,
    WORK_ROLE_OPTIONS,
    Question,
    get_type_questions,
)
from sie.enneagram.scoring import score_center
from sie.enneagram.types import Center, get_type_info

TOTAL_STEPS = 5

STEP_TITLES = {
    1: "Step 1 — センター判定",
    2: "Step 2 — タイプ判定",
    3: "Step 3 — ウイング判定",
    4: "Step 4 — 本能サブタイプ",
    5: "追加情報（精度向上）",
}

CATEGORY_LABELS = {
    "reaction": "反応の仕方",
    "attention": "注意の向き",
    "emotion": "感情の扱い方",
    "action_priority": "行動の優先順位",
    "motivation": "動機",
    "fear": "恐れ",
    "desire": "欲求",
    "behavior_pattern": "行動パターン",
    "extraversion": "外向 / 内向",
    "action_direction": "行動の方向性",
    "expression_texture": "表現の質感",
    "safety": "安全（sp）",
    "role": "役割（so）",
    "intimacy": "親密（sx）",
}

CENTER_LABELS = {
    Center.BODY: "本能センター（タイプ 8・9・1）",
    Center.HEART: "感情センター（タイプ 2・3・4）",
    Center.HEAD: "思考センター（タイプ 5・6・7）",
}

TRAIT_LABELS = {
    "assertive": "自己主張が強い",
    "emotional": "感情豊か",
    "analytical": "分析的",
    "helpful": "助人的",
    "peaceful": "穏やか",
    "ambitious": "野心がある",
    "unique": "独自性を大切にする",
    "cautious": "慎重",
}

INSTINCT_LABELS = {"sp": "自己保存（sp）", "so": "社会（so）", "sx": "性/親密（sx）"}


def _init_assessment_state() -> None:
    defaults = {
        "assessment_step": 1,
        "center_answers": {},
        "type_answers": {},
        "wing_answers": {},
        "instinct_answers": {},
        "episode_conflict": "",
        "episode_values": "",
        "episode_emotions": "",
        "behavior_work": 0,
        "behavior_relation": 0,
        "behavior_stress": 0,
        "self_traits": {k: 5 for k in TRAIT_LABELS},
        "other_traits": {k: 5 for k in TRAIT_LABELS},
        "episode_samples": [],
        "assessment_editing": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_assessment() -> None:
    for key in (
        "assessment_step",
        "center_answers",
        "type_answers",
        "wing_answers",
        "instinct_answers",
        "episode_conflict",
        "episode_values",
        "episode_emotions",
        "behavior_work",
        "behavior_relation",
        "behavior_stress",
        "self_traits",
        "other_traits",
        "episode_samples",
        "enneagram_profile",
        "assessment_editing",
        "enneagram_saved",
    ):
        st.session_state.pop(key, None)
    _init_assessment_state()
    st.session_state.assessment_editing = True


def save_profile_and_talk() -> None:
    """Keep diagnosis result and switch to S.I.E. conversation."""
    profile = st.session_state.enneagram_profile
    st.session_state.enneagram_saved = True
    if "sie_session" in st.session_state:
        st.session_state.sie_session.enneagram = profile
    st.session_state.app_mode = "会話"
    st.rerun()


def redo_assessment() -> None:
    """Restart the questionnaire from step 1."""
    reset_assessment()
    st.session_state.app_mode = "エニアグラム診断"
    st.rerun()


def request_full_initialize() -> None:
    """Reset diagnosis and S.I.E. session to the initial state."""
    reset_assessment()
    st.session_state.full_initialize_requested = True
    st.rerun()


def _render_result_actions() -> None:
    st.divider()
    st.markdown("### 次にすること")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("結果を保持したまま会話へ")
        if st.button(
            "① サイと会話する",
            use_container_width=True,
            type="primary",
            key="action_talk_with_sie",
        ):
            save_profile_and_talk()

    with col2:
        st.caption("回答を消して最初から")
        if st.button(
            "② 診断をやり直す",
            use_container_width=True,
            key="action_redo_assessment",
        ):
            redo_assessment()

    with col3:
        st.caption("診断・会話をすべてリセット")
        if st.button(
            "③ 初期化",
            use_container_width=True,
            key="action_full_initialize",
        ):
            request_full_initialize()


def _questions_complete(questions: tuple[Question, ...], answers: dict[str, int]) -> bool:
    return all(q.id in answers for q in questions)


def _render_questions_by_category(
    questions: tuple[Question, ...],
    answers: dict[str, int],
    key_prefix: str,
) -> dict[str, int]:
    """Render radio groups and return updated answers."""
    by_category: dict[str, list[Question]] = {}
    for question in questions:
        by_category.setdefault(question.category, []).append(question)

    for category, category_questions in by_category.items():
        st.markdown(f"#### {CATEGORY_LABELS.get(category, category)}")
        for question in category_questions:
            options = [opt.text for opt in question.options]
            current = answers.get(question.id, 0)
            selected = st.radio(
                question.text,
                range(len(options)),
                index=current,
                format_func=lambda i, opts=options: opts[i],
                key=f"{key_prefix}_{question.id}",
            )
            answers[question.id] = selected
        st.divider()

    return answers


def _render_step1() -> None:
    st.markdown("### 本能・感情・思考、どのセンターが最も強いか")
    st.caption("15問 — 反応・注意・感情・行動の優先順位")
    st.session_state.center_answers = _render_questions_by_category(
        CENTER_QUESTIONS,
        st.session_state.center_answers,
        "center",
    )


def _render_step2() -> None:
    center = score_center(st.session_state.center_answers)
    questions = get_type_questions(center)
    st.markdown(f"### {CENTER_LABELS[center]}")
    st.caption("9問 — 動機・恐れ・欲求・行動パターン")
    st.session_state.type_answers = _render_questions_by_category(
        questions,
        st.session_state.type_answers,
        "type",
    )


def _render_step3() -> None:
    st.markdown("### ウイング（隣接タイプの傾向）")
    st.caption("6問 — 外向/内向・方向性・表現")
    st.session_state.wing_answers = _render_questions_by_category(
        WING_QUESTIONS,
        st.session_state.wing_answers,
        "wing",
    )


def _render_step4() -> None:
    st.markdown("### 本能サブタイプ（sp / so / sx）")
    st.caption("12問 — 安全・役割・親密、どれを優先するか")
    st.session_state.instinct_answers = _render_questions_by_category(
        INSTINCT_QUESTIONS,
        st.session_state.instinct_answers,
        "instinct",
    )


def _render_step5() -> None:
    st.markdown("### 追加情報")
    st.caption("任意ですが、入力すると診断精度が上がります。")

    st.markdown("#### エピソード（自由記述）")
    st.session_state.episode_conflict = st.text_area(
        "最近の衝突やモヤモヤした出来事",
        value=st.session_state.episode_conflict,
        height=80,
    )
    st.session_state.episode_values = st.text_area(
        "大事にしている価値観",
        value=st.session_state.episode_values,
        height=80,
    )
    st.session_state.episode_emotions = st.text_area(
        "怒り・不安・悲しみの扱い方",
        value=st.session_state.episode_emotions,
        height=80,
    )

    st.markdown("#### 行動ログ（選択式）")
    st.session_state.behavior_work = st.selectbox(
        "仕事での役割に近いもの",
        range(len(WORK_ROLE_OPTIONS)),
        format_func=lambda i: WORK_ROLE_OPTIONS[i],
        index=st.session_state.behavior_work,
    )
    st.session_state.behavior_relation = st.selectbox(
        "人間関係の傾向",
        range(len(RELATIONSHIP_OPTIONS)),
        format_func=lambda i: RELATIONSHIP_OPTIONS[i],
        index=st.session_state.behavior_relation,
    )
    st.session_state.behavior_stress = st.selectbox(
        "ストレス時の反応",
        range(len(STRESS_REACTION_OPTIONS)),
        format_func=lambda i: STRESS_REACTION_OPTIONS[i],
        index=st.session_state.behavior_stress,
    )

    st.markdown("#### 自己評価 vs 他者評価（1〜10）")
    st.caption("ズレが大きいほど、タイプ判定の重要指標になります。")
    col_self, col_other = st.columns(2)
    with col_self:
        st.markdown("**自分が思う自分**")
        for trait, label in TRAIT_LABELS.items():
            st.session_state.self_traits[trait] = st.slider(
                label,
                1,
                10,
                st.session_state.self_traits[trait],
                key=f"self_{trait}",
            )
    with col_other:
        st.markdown("**他者から見た自分**")
        for trait, label in TRAIT_LABELS.items():
            st.session_state.other_traits[trait] = st.slider(
                label,
                1,
                10,
                st.session_state.other_traits[trait],
                key=f"other_{trait}",
            )

    st.markdown("#### エピソード詳細（任意）")
    with st.expander("出来事を1件追加"):
        event = st.text_input("出来事")
        feeling = st.text_input("そのときの感情")
        action = st.text_input("取った行動")
        result = st.text_input("結果")
        if st.button("エピソードを追加", key="add_episode"):
            if event.strip():
                st.session_state.episode_samples.append(
                    EpisodeSample(
                        event=event.strip(),
                        feeling=feeling.strip(),
                        action=action.strip(),
                        result=result.strip(),
                    )
                )
                st.success("追加しました")
                st.rerun()

    if st.session_state.episode_samples:
        for i, sample in enumerate(st.session_state.episode_samples):
            st.markdown(
                f"- **{sample['event']}** — {sample['feeling']} → "
                f"{sample['action']}（{sample['result']}）"
            )


def _build_assessment_input() -> AssessmentInput:
    return AssessmentInput(
        center_answers=st.session_state.center_answers,
        type_answers=st.session_state.type_answers,
        wing_answers=st.session_state.wing_answers,
        instinct_answers=st.session_state.instinct_answers,
        episodes=EpisodeInput(
            recent_conflict=st.session_state.episode_conflict,
            core_values=st.session_state.episode_values,
            emotion_handling=st.session_state.episode_emotions,
        ),
        behavior_log=BehaviorLog(
            work_role=st.session_state.behavior_work,
            relationship_tendency=st.session_state.behavior_relation,
            stress_reaction=st.session_state.behavior_stress,
        ),
        self_other_gap=SelfOtherGap(
            self_image=dict(st.session_state.self_traits),
            others_image=dict(st.session_state.other_traits),
        ),
        episode_samples=list(st.session_state.episode_samples),
    )


def _validate_current_step(step: int) -> list[str]:
    if step == 1:
        if not _questions_complete(CENTER_QUESTIONS, st.session_state.center_answers):
            return ["すべてのセンター判定の質問に回答してください。"]
    elif step == 2:
        center = score_center(st.session_state.center_answers)
        questions = get_type_questions(center)
        if not _questions_complete(questions, st.session_state.type_answers):
            return ["すべてのタイプ判定の質問に回答してください。"]
    elif step == 3:
        if not _questions_complete(WING_QUESTIONS, st.session_state.wing_answers):
            return ["すべてのウイング判定の質問に回答してください。"]
    elif step == 4:
        if not _questions_complete(INSTINCT_QUESTIONS, st.session_state.instinct_answers):
            return ["すべての本能判定の質問に回答してください。"]
    return []


def _render_results() -> None:
    profile = st.session_state.enneagram_profile
    type_info = get_type_info(profile.primary_type)

    st.success("診断が完了しました")
    st.markdown(f"## {type_info.name}")
    if profile.wing:
        st.markdown(f"**ウイング:** タイプ {profile.wing}")
    st.markdown(
        f"**本能サブタイプ:** {INSTINCT_LABELS.get(profile.instinctual_variant, profile.instinctual_variant)}"
    )

    if profile.reasoning:
        st.markdown("### 判定の根拠")
        st.caption("なぜこのタイプ・ウイングになったか")
        for line in profile.reasoning:
            st.markdown(f"- {line}")

    st.markdown('<div class="enneagram-result">', unsafe_allow_html=True)
    st.markdown(f"**概要:** {profile.summary}")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**強み**")
        for item in profile.strengths:
            st.markdown(f"- {item}")
        st.markdown("**コアの恐れ**")
        st.markdown(profile.core_fear)
        st.markdown("**ストレス時の型**")
        st.markdown(f"タイプ {profile.stress_pattern}")
    with col2:
        st.markdown("**盲点**")
        for item in profile.blind_spots:
            st.markdown(f"- {item}")
        st.markdown("**コアの欲求**")
        st.markdown(profile.core_desire)
        st.markdown("**成長時の型**")
        st.markdown(f"タイプ {profile.growth_pattern}")

    st.markdown("**コミュニケーション**")
    st.markdown(profile.communication_style)
    st.markdown("**対立パターン**")
    st.markdown(profile.conflict_pattern)
    st.markdown("**関係で必要なもの**")
    for item in profile.relationship_needs:
        st.markdown(f"- {item}")

    if profile.childhood_wound:
        st.markdown("**幼少期の傷（傾向）**")
        st.markdown(profile.childhood_wound)

    st.markdown("**タイプ別スコア（参考）**")
    st.caption("補足データを含めた参考値です。ウイング判定とは別の指標です。")
    score_text = " · ".join(
        f"{t}: {profile.scores.get(t, 0):.0%}" for t in range(1, 10)
    )
    st.caption(score_text)

    if profile.episode_samples:
        st.markdown("**記録したエピソード**")
        for sample in profile.episode_samples:
            st.markdown(f"- {sample['event']}")

    _render_result_actions()

    st.divider()
    st.markdown("### 結果をメールで受け取る")
    st.caption("入力したアドレスに、診断結果の全文を送信します。")
    email_address = st.text_input(
        "メールアドレス",
        placeholder="example@gmail.com",
        key="enneagram_result_email",
    )
    if st.button("診断結果をメール送信", use_container_width=True):
        if not email_address.strip():
            st.error("メールアドレスを入力してください。")
        else:
            from sie.email import send_enneagram_result_email

            try:
                with st.spinner("送信中…"):
                    send_enneagram_result_email(email_address, profile)
                st.success(f"{email_address.strip()} に送信しました。")
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"送信に失敗しました: {exc}")


def render_enneagram_assessment() -> None:
    """Render the full multi-step Enneagram assessment UI."""
    _init_assessment_state()

    if st.session_state.get("enneagram_profile") and not st.session_state.get(
        "assessment_editing", True
    ):
        st.title("エニアグラム性格診断")
        _render_results()
        return

    st.title("エニアグラム性格診断")
    st.caption(
        "18歳より前の経験（学校・家庭・友達）を思い出して答えてください。"
        "社会人としての「正解」ではなく、当時の自然な反応を選んでください。"
    )

    step = st.session_state.assessment_step
    st.progress(step / (TOTAL_STEPS + 1))
    st.markdown(f"### {STEP_TITLES.get(step, '結果')}")

    if step == 1:
        _render_step1()
    elif step == 2:
        _render_step2()
    elif step == 3:
        _render_step3()
    elif step == 4:
        _render_step4()
    elif step == 5:
        _render_step5()

    st.divider()
    nav_prev, nav_mid, nav_next = st.columns([1, 2, 1])

    with nav_prev:
        if step > 1 and st.button("← 戻る", use_container_width=True):
            st.session_state.assessment_step -= 1
            st.rerun()

    with nav_mid:
        if st.button("最初からやり直す", use_container_width=True):
            reset_assessment()
            st.session_state.assessment_editing = True
            st.rerun()

    with nav_next:
        if step < TOTAL_STEPS:
            if st.button("次へ →", use_container_width=True, type="primary"):
                errors = _validate_current_step(step)
                if errors:
                    for err in errors:
                        st.error(err)
                else:
                    st.session_state.assessment_step += 1
                    st.rerun()
        elif step == TOTAL_STEPS:
            if st.button("診断結果を見る", use_container_width=True, type="primary"):
                try:
                    st.session_state.enneagram_profile = run_assessment(
                        _build_assessment_input()
                    )
                    st.session_state.assessment_editing = False
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
