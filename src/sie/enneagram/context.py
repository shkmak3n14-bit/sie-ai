"""Build LLM internal instructions from Enneagram profile."""

from __future__ import annotations

from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.types import get_type_info
from sie.enneagram.wing_templates import format_wing_template_instruction, get_wing_template
from sie.flow import ConversationPhase
from sie.session import Session

INSTINCT_LABELS = {
    "sp": "自己保存（sp）",
    "so": "社会（so）",
    "sx": "性/親密（sx）",
}


def _format_profile_summary(profile: EnneagramProfile) -> str:
    type_info = get_type_info(profile.primary_type)
    wing_text = f"、ウイング {profile.wing}" if profile.wing else ""
    instinct = INSTINCT_LABELS.get(profile.instinctual_variant, profile.instinctual_variant)

    strengths = "、".join(profile.strengths)
    blind_spots = "、".join(profile.blind_spots)
    needs = "、".join(profile.relationship_needs)

    return (
        f"エニアグラム: {type_info.name}{wing_text}、本能 {instinct}。\n"
        f"概要: {profile.summary}\n"
        f"強み: {strengths}。\n"
        f"盲点: {blind_spots}。\n"
        f"コアの恐れ: {profile.core_fear}。\n"
        f"コアの欲求: {profile.core_desire}。\n"
        f"コミュニケーション: {profile.communication_style}\n"
        f"対立パターン: {profile.conflict_pattern}\n"
        f"関係で必要なもの: {needs}。\n"
        f"ストレス時はタイプ{profile.stress_pattern}の傾向、"
        f"成長時はタイプ{profile.growth_pattern}の傾向。\n"
        f"幼少期の傷（傾向）: {profile.childhood_wound or '—'}"
    )


def _behavior_rules() -> str:
    return (
        "タイプ番号や診断用語を押し付けず、相手の言葉とエピソードに沿って静かに核心を伝える。"
        "「あなたはタイプ◯」と決めつけない。"
    )


def _wing_template_block(profile: EnneagramProfile) -> str:
    template = get_wing_template(profile.primary_type, profile.wing)
    if template is None:
        return ""
    return format_wing_template_instruction(template) + "\n"


def get_enneagram_instruction(session: Session) -> str | None:
    """Return phase-appropriate internal instruction, or None if no profile."""
    profile = session.enneagram
    if profile is None:
        return None

    phase = session.phase
    summary = _format_profile_summary(profile)
    rules = _behavior_rules()

    if phase == ConversationPhase.CORE:
        episodes = ""
        if profile.episode_samples:
            lines = [
                f"・{s['event']}（{s['feeling']}→{s['action']}）"
                for s in profile.episode_samples[:3]
            ]
            episodes = "\n記録エピソード:\n" + "\n".join(lines)

        return (
            f"[エニアグラム診断結果を核心フェーズで加味]\n{summary}{episodes}\n"
            f"{_wing_template_block(profile)}"
            f"{rules} "
            "役割と気性の話と結びつけ、恐れ・欲求・盲点を相手のペースで静かに映す。"
        )

    if phase == ConversationPhase.EMPATHY:
        wing_block = _wing_template_block(profile)
        return (
            f"[エニアグラム診断結果を寄り添いで加味]\n"
            f"コミュニケーション: {profile.communication_style}\n"
            f"関係で必要なもの: {', '.join(profile.relationship_needs)}。\n"
            f"{wing_block}"
            f"{rules}"
        )

    if phase == ConversationPhase.GUIDANCE:
        return (
            f"[エニアグラム診断結果を導きで加味]\n"
            f"盲点: {', '.join(profile.blind_spots)}。\n"
            f"ストレス時タイプ{profile.stress_pattern}、成長時タイプ{profile.growth_pattern}。\n"
            f"{_wing_template_block(profile)}"
            f"{rules} 自己理解から他者理解への橋渡しに活かす。"
        )

    if phase in (ConversationPhase.ONGOING, ConversationPhase.CLOSING):
        return (
            f"[エニアグラム診断結果]\n{summary}\n"
            f"{_wing_template_block(profile)}"
            f"{rules}"
        )

    return None
