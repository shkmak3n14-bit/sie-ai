"""Relationship episode collection and analysis instructions."""

from __future__ import annotations

from dataclasses import dataclass

RELATIONSHIP_ROLES: tuple[str, ...] = (
    "友人",
    "恋人",
    "上司",
    "部下",
    "同僚",
    "家族",
    "あなた",
    "その他",
)


@dataclass
class RelationshipEpisode:
    subject_name: str
    subject_role: str
    target_name: str
    target_role: str
    action: str
    user_reaction: str


def format_episode_user_message(episode: RelationshipEpisode) -> str:
    """Format the episode as a user message for the chat history."""
    subject = f"{episode.subject_name}さん（{episode.subject_role}）"
    target = f"{episode.target_name}さん（{episode.target_role}）"
    return (
        "【エピソード共有】\n"
        f"{subject}が、{target}に、{episode.action}\n"
        f"あなたは：{episode.user_reaction}"
    )


def get_episode_analysis_instruction(episode: RelationshipEpisode) -> str:
    """Return internal LLM instruction for episode analysis."""
    focus_name = episode.subject_name
    return (
        "[エピソード分析モード]\n"
        f"共有されたエピソードについて、{focus_name}さんを主な分析対象として、"
        "S.I.E.（サイ）の落ち着いたトーンで、以下の6観点を必ず順番に含めて回答してください。"
        "見出し番号（①〜⑥）を付け、各観点を自然な日本語で丁寧に述べてください。\n"
        f"① 想定される{focus_name}さんの性格\n"
        "② その論拠（エピソードのどの部分からそう読み取るか）\n"
        "③ どのような情報があれば精度が高くなるか\n"
        f"④ 想定される{focus_name}さんのレッドライン（絶対に踏んではいけない一線）\n"
        "⑤ お互いのレッドラインに対する現状分析（あなたと相手の両方）\n"
        "⑥ どうすればお互いに好循環になるのか（具体的で実行可能な提案）\n"
        "決めつけず、仮説として静かに伝えること。"
        "エニアグラムのタイプ番号を押し付けない。"
        "相手の関係性（友人・恋人・上司など）を踏まえること。"
    )
