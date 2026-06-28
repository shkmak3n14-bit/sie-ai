"""Tests for relationship episode analysis."""

from sie.episode import (
    RelationshipEpisode,
    format_episode_user_message,
    get_episode_analysis_instruction,
)


def test_format_episode_user_message() -> None:
    episode = RelationshipEpisode(
        subject_name="太郎",
        subject_role="上司",
        target_name="花子",
        target_role="部下",
        action="厳しい口調で注意した",
        user_reaction="黙って受け止めた",
    )
    text = format_episode_user_message(episode)
    assert "太郎さん（上司）" in text
    assert "花子さん（部下）" in text
    assert "厳しい口調で注意した" in text
    assert "黙って受け止めた" in text


def test_episode_analysis_instruction_covers_six_points() -> None:
    episode = RelationshipEpisode(
        subject_name="太郎",
        subject_role="友人",
        target_name="あなた",
        target_role="あなた",
        action="test",
        user_reaction="test",
    )
    instruction = get_episode_analysis_instruction(episode)
    assert "①" in instruction
    assert "⑥" in instruction
    assert "太郎さん" in instruction
    assert "レッドライン" in instruction
    assert "好循環" in instruction
