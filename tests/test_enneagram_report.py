"""Tests for Enneagram email report formatting."""

from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.report import format_report_html, format_report_plain


def _sample_profile() -> EnneagramProfile:
    return EnneagramProfile(
        primary_type=5,
        wing=4,
        scores={n: 0.1 for n in range(1, 10)},
        summary="知識と内省を通じて世界を理解する。",
        strengths=["分析力", "客観性"],
        blind_spots=["孤立", "感情の切り離し"],
        stress_pattern=7,
        growth_pattern=8,
        instinctual_variant="sp",
        core_fear="無能で、支援も世界もないこと",
        core_desire="有能であり、世界を理解すること",
        communication_style="簡潔で論理的。",
        conflict_pattern="圧倒されると引きこもる。",
        relationship_needs=["個人的な時間", "信頼"],
        childhood_wound="世界は要求が多すぎる。",
        episode_samples=[
            {
                "event": "テストで失点",
                "feeling": "不安",
                "action": "一人で復習",
                "result": "理解が深まった",
            }
        ],
    )


def test_format_report_plain_includes_key_fields() -> None:
    text = format_report_plain(_sample_profile())
    assert "タイプ5" in text
    assert "ウイング: タイプ 4" in text
    assert "分析力" in text
    assert "テストで失点" in text


def test_format_report_html_includes_key_fields() -> None:
    html = format_report_html(_sample_profile())
    assert "<h2>" in html
    assert "タイプ5" in html
    assert "分析力" in html
