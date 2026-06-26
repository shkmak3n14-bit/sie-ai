"""Format Enneagram assessment results for email delivery."""

from __future__ import annotations

from sie.enneagram.confidence import format_confidence_lines, low_confidence_messages
from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.types import get_type_info
from sie.enneagram.wing_templates import format_wing_template_report, get_wing_template

INSTINCT_LABELS = {
    "sp": "自己保存（sp）",
    "so": "社会（so）",
    "sx": "性/親密（sx）",
}


def _bullet_lines(items: list[str]) -> str:
    return "\n".join(f"  ・{item}" for item in items)


def format_report_plain(profile: EnneagramProfile) -> str:
    """Return a plain-text report suitable for email."""
    type_info = get_type_info(profile.primary_type)
    instinct = INSTINCT_LABELS.get(profile.instinctual_variant, profile.instinctual_variant)
    wing_line = f"ウイング: タイプ {profile.wing}\n" if profile.wing else ""
    confidence_lines = format_confidence_lines(profile)
    confidence_block = "\n".join(confidence_lines) + "\n" if confidence_lines else ""
    warning_lines = low_confidence_messages(profile)
    warning_block = (
        "\n".join(f"※ {msg}" for msg in warning_lines) + "\n" if warning_lines else ""
    )

    scores = " / ".join(
        f"タイプ{t} {profile.scores.get(t, 0):.0%}" for t in range(1, 10)
    )

    lines = [
        "S.I.E. エニアグラム性格診断 — 結果",
        "=" * 40,
        "",
        type_info.name,
        wing_line.rstrip(),
        confidence_block.rstrip(),
        warning_block.rstrip(),
        f"本能サブタイプ: {instinct}",
        "",
        "【概要】",
        profile.summary,
        "",
        "【強み】",
        _bullet_lines(profile.strengths),
        "",
        "【盲点】",
        _bullet_lines(profile.blind_spots),
        "",
        "【コアの恐れ】",
        profile.core_fear,
        "",
        "【コアの欲求】",
        profile.core_desire,
        "",
        "【コミュニケーション】",
        profile.communication_style,
        "",
        "【対立パターン】",
        profile.conflict_pattern,
        "",
        "【関係で必要なもの】",
        _bullet_lines(profile.relationship_needs),
        "",
        f"【ストレス時の型】タイプ {profile.stress_pattern}",
        f"【成長時の型】タイプ {profile.growth_pattern}",
    ]

    if profile.childhood_wound:
        lines.extend(["", "【幼少期の傷（傾向）】", profile.childhood_wound])

    wing_template = get_wing_template(profile.primary_type, profile.wing)
    if wing_template:
        lines.extend(["", *format_wing_template_report(wing_template)])

    lines.extend(["", "【タイプ別スコア（参考）】", scores])

    if profile.reasoning:
        lines.extend(["", "【判定の根拠】"])
        for item in profile.reasoning:
            lines.append(f"  ・{item}")

    if profile.episode_samples:
        lines.extend(["", "【記録したエピソード】"])
        for sample in profile.episode_samples:
            lines.append(
                f"  ・{sample['event']} — {sample['feeling']} → "
                f"{sample['action']}（{sample['result']}）"
            )

    lines.extend(
        [
            "",
            "-" * 40,
            "Support Intelligence on Ego — S.I.E.（サイ）",
        ]
    )
    return "\n".join(line for line in lines if line is not None)


def format_report_html(profile: EnneagramProfile) -> str:
    """Return an HTML report suitable for email."""
    type_info = get_type_info(profile.primary_type)
    instinct = INSTINCT_LABELS.get(profile.instinctual_variant, profile.instinctual_variant)

    def lis(items: list[str]) -> str:
        return "".join(f"<li>{item}</li>" for item in items)

    wing_html = f"<p><strong>ウイング:</strong> タイプ {profile.wing}</p>" if profile.wing else ""
    confidence_html = "".join(f"<li>{line}</li>" for line in format_confidence_lines(profile))
    confidence_section = (
        f"<h3>判定信頼度</h3><ul>{confidence_html}</ul>" if confidence_html else ""
    )
    warnings = low_confidence_messages(profile)
    warning_html = "".join(f"<li>{msg}</li>" for msg in warnings)
    warning_section = (
        f"<h3>参考</h3><ul>{warning_html}</ul>" if warning_html else ""
    )
    wound_html = (
        f"<h3>幼少期の傷（傾向）</h3><p>{profile.childhood_wound}</p>"
        if profile.childhood_wound
        else ""
    )

    wing_template = get_wing_template(profile.primary_type, profile.wing)
    wing_template_html = ""
    if wing_template:

        def lis_tuple(items: tuple[str, ...]) -> str:
            return "".join(f"<li>{item}</li>" for item in items)

        wing_template_html = f"""\
  <h3>ウイング人格: {wing_template.type} — {wing_template.label}</h3>
  <h4>判断基準</h4>
  <ul>{lis_tuple(wing_template.judgment_criteria)}</ul>
  <h4>推論ルール</h4>
  <ul>{lis_tuple(wing_template.inference_rules)}</ul>
  <h4>行動原理</h4>
  <ul>{lis_tuple(wing_template.behavior_principles)}</ul>
  <h4>価値プロフィール</h4>
  <ul>{lis_tuple(wing_template.value_profile)}</ul>"""

    scores_html = " · ".join(
        f"タイプ{t} {profile.scores.get(t, 0):.0%}" for t in range(1, 10)
    )

    episodes_html = ""
    if profile.episode_samples:
        items = "".join(
            f"<li>{s['event']} — {s['feeling']} → {s['action']}（{s['result']}）</li>"
            for s in profile.episode_samples
        )
        episodes_html = f"<h3>記録したエピソード</h3><ul>{items}</ul>"

    reasoning_html = ""
    if profile.reasoning:
        items = "".join(f"<li>{line}</li>" for line in profile.reasoning)
        reasoning_html = f"<h3>判定の根拠</h3><ul>{items}</ul>"

    return f"""\
<!DOCTYPE html>
<html lang="ja">
<body style="font-family: sans-serif; color: #222; line-height: 1.6;">
  <h1 style="color: #4a6fa5;">S.I.E. エニアグラム性格診断</h1>
  <h2>{type_info.name}</h2>
  {wing_html}
  <p><strong>本能サブタイプ:</strong> {instinct}</p>
  {confidence_section}
  {warning_section}
  <h3>概要</h3>
  <p>{profile.summary}</p>
  <h3>強み</h3>
  <ul>{lis(profile.strengths)}</ul>
  <h3>盲点</h3>
  <ul>{lis(profile.blind_spots)}</ul>
  <h3>コアの恐れ</h3>
  <p>{profile.core_fear}</p>
  <h3>コアの欲求</h3>
  <p>{profile.core_desire}</p>
  <h3>コミュニケーション</h3>
  <p>{profile.communication_style}</p>
  <h3>対立パターン</h3>
  <p>{profile.conflict_pattern}</p>
  <h3>関係で必要なもの</h3>
  <ul>{lis(profile.relationship_needs)}</ul>
  <p><strong>ストレス時の型:</strong> タイプ {profile.stress_pattern}</p>
  <p><strong>成長時の型:</strong> タイプ {profile.growth_pattern}</p>
  {wound_html}
  {wing_template_html}
  {reasoning_html}
  <h3>タイプ別スコア（参考）</h3>
  <p>{scores_html}</p>
  {episodes_html}
  <hr>
  <p style="color: #666; font-size: 0.9em;">Support Intelligence on Ego — S.I.E.（サイ）</p>
</body>
</html>"""
