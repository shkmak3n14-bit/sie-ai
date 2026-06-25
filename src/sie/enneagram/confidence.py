"""Confidence scores and formatted display for assessment results."""

from __future__ import annotations

from sie.enneagram.profile import EnneagramProfile

LOW_CONFIDENCE_THRESHOLD = 0.55


def normalize_shares(totals: dict) -> dict:
    """Return each key's share of the total (0.0–1.0)."""
    total = sum(totals.values()) or 1.0
    return {k: v / total for k, v in totals.items()}


def winner_confidence(totals: dict) -> float:
    """Return the winning entry's share of the total."""
    if not totals:
        return 0.0
    total = sum(totals.values()) or 1.0
    return max(totals.values()) / total


def wing_confidence_detail(
    wing_low: int,
    wing_high: int,
    wing_totals: dict[str, float],
) -> tuple[float, dict[int, float]]:
    """Return wing confidence and per-wing shares."""
    low_score = wing_totals.get("wing_low", 0.0)
    high_score = wing_totals.get("wing_high", 0.0)
    total = low_score + high_score
    if total <= 0:
        return 0.0, {wing_low: 0.0, wing_high: 0.0}
    return max(low_score, high_score) / total, {
        wing_low: low_score / total,
        wing_high: high_score / total,
    }


def format_confidence_lines(profile: EnneagramProfile) -> list[str]:
    """Return the three confidence summary lines for display."""
    lines: list[str] = []

    cs = profile.center_shares
    lines.append(
        f"センター信頼度：{profile.center_confidence:.0%}"
        f"（本能_{cs.get('body', 0):.0%} vs 思考_{cs.get('head', 0):.0%}"
        f" vs 感情_{cs.get('heart', 0):.0%}）"
    )

    type_parts = " vs ".join(
        f"{t}_{profile.type_shares_in_center.get(t, 0):.0%}"
        for t in profile.type_share_order
    )
    lines.append(f"主タイプ信頼度：{profile.type_confidence:.0%}（{type_parts}）")

    if profile.wing is not None and profile.wing_shares:
        wing_parts = " vs ".join(
            f"w{t}_{profile.wing_shares.get(t, 0):.0%}"
            for t in profile.wing_share_order
        )
        lines.append(f"ウイング信頼度：{profile.wing_confidence:.0%}（{wing_parts}）")

    return lines


def low_confidence_messages(profile: EnneagramProfile) -> list[str]:
    """Return user-facing warnings for any low-confidence dimension."""
    messages: list[str] = []
    if profile.center_low_confidence:
        messages.append(
            "センター判定の信頼度がやや低めです。"
            "本能・感情・思考のどれが強いか迷う場合は、時間を置いて再診断してください。"
        )
    if profile.type_low_confidence:
        messages.append(
            "主タイプ判定の信頼度がやや低めです。"
            "タイプの当たり外れを感じる場合は、時間を置いて再診断することをおすすめします。"
        )
    if profile.wing_low_confidence:
        messages.append(
            "ウイング判定の信頼度がやや低めです。"
            "w の当たり外れを感じる場合は、ウイング質問を意識して再診断してください。"
        )
    if profile.type_supplemental_only:
        messages.append(
            "センター判定が変更されたため、タイプは補足データ中心の参考値です。"
            "次回は Step 2c のタイプ再確認まで完了すると精度が上がります。"
        )
    return messages
