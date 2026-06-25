"""Build human-readable rationale for assessment results."""

from __future__ import annotations

from sie.enneagram.types import CENTER_TYPES, Center, wing_types

CENTER_LABELS = {
    Center.BODY: "本能センター（タイプ 8・9・1）",
    Center.HEART: "感情センター（タイプ 2・3・4）",
    Center.HEAD: "思考センター（タイプ 5・6・7）",
}

INSTINCT_LABELS = {"sp": "自己保存（sp）", "so": "社会（so）", "sx": "性/親密（sx）"}


def _pct(value: float, total: float) -> str:
    if total <= 0:
        return "0%"
    return f"{value / total:.0%}"


def build_reasoning(
    *,
    center: Center,
    center_totals: dict[str, float],
    center_confidence: float,
    center_tiebreak_used: bool,
    center_tiebreak_pair: tuple[Center, Center] | None,
    question_primary: int,
    refined_primary: int,
    type_totals_in_center: dict[int, float],
    supplemental_type: dict[int, float],
    wing: int,
    wing_low: int,
    wing_high: int,
    wing_totals: dict[str, float],
    instinct_variant: str,
    instinct_totals: dict[str, float],
    normalized_scores: dict[int, float],
) -> list[str]:
    """Return bullet-point explanations for how the result was determined."""
    lines: list[str] = []

    center_total = sum(center_totals.values()) or 1.0
    conf_pct = f"{center_confidence:.0%}"
    lines.append(
        f"【Step 1 センター】{CENTER_LABELS[center]} が最も高く、"
        f"本能 {center_totals.get('body', 0):.0f} / "
        f"感情 {center_totals.get('heart', 0):.0f} / "
        f"思考 {center_totals.get('head', 0):.0f} "
        f"（判定信頼度 {conf_pct}）でした。"
    )
    if center_tiebreak_used and center_tiebreak_pair:
        a, b = center_tiebreak_pair
        labels = {
            Center.BODY: "本能",
            Center.HEART: "感情",
            Center.HEAD: "思考",
        }
        lines.append(
            f"【Step 1b センター追加判定】"
            f"{labels[a]}と{labels[b]}が接戦だったため、追加5問で判別しました。"
        )
    elif center_confidence < 0.55:
        lines.append(
            "【センター判定】得点差が小さく、センター判定の信頼度はやや低めです。"
            "結果がしっくりこない場合は、時間を置いて再診断することをおすすめします。"
        )

    type_in_center_total = sum(type_totals_in_center.values()) or 1.0
    type_parts = " · ".join(
        f"タイプ{t} {_pct(v, type_in_center_total)}"
        for t, v in sorted(type_totals_in_center.items())
    )
    lines.append(
        f"【Step 2 タイプ（センター内）】質問回答のみではタイプ {question_primary} が最高（{type_parts}）。"
    )

    if question_primary != refined_primary:
        lines.append(
            f"【補足データの反映】エピソード・行動ログ・自己/他者評価を加味し、"
            f"最終的な主タイプをタイプ {refined_primary} に調整しました。"
        )
    else:
        supp_in_center = {
            t: v for t, v in supplemental_type.items() if t in CENTER_TYPES[center]
        }
        if any(v > 0 for v in supp_in_center.values()):
            parts = "、".join(
                f"タイプ{t}+{v:.1f}" for t, v in sorted(supp_in_center.items()) if v > 0
            )
            lines.append(f"【補足データ】センター内タイプへの加点: {parts}。")
        lines.append(f"【主タイプ】タイプ {refined_primary} と判定しました。")

    wing_total = sum(wing_totals.values()) or 1.0
    low_score = wing_totals.get("wing_low", 0)
    high_score = wing_totals.get("wing_high", 0)
    lines.append(
        f"【Step 3 ウイング】タイプ {refined_primary} の隣接タイプは {wing_low} と {wing_high} です。"
        f"ウイング質問ではタイプ {wing_low} 側 {_pct(low_score, wing_total)} / "
        f"タイプ {wing_high} 側 {_pct(high_score, wing_total)} のため、"
        f"ウイング {wing} → {refined_primary}w{wing} としました。"
    )
    lines.append(
        "※ウイングの数字（例: w7）はタイプ7の性格そのものではなく、"
        "主タイプに隣接する傾向を示します。そのためタイプ別スコアのタイプ7が低くても w7 になることがあります。"
    )

    instinct_total = sum(instinct_totals.values()) or 1.0
    instinct_parts = " · ".join(
        f"{INSTINCT_LABELS.get(k, k)} {_pct(v, instinct_total)}"
        for k, v in sorted(instinct_totals.items())
    )
    lines.append(
        f"【Step 4 本能】{instinct_parts} → "
        f"{INSTINCT_LABELS.get(instinct_variant, instinct_variant)} と判定。"
    )

    body_types = CENTER_TYPES[center]
    norm_parts = " · ".join(
        f"タイプ{t} {normalized_scores.get(t, 0):.0%}" for t in range(1, 10)
    )
    lines.append(
        "【タイプ別スコア（参考）】表示の % は、主タイプへの固定加点と"
        "エピソード等の補足データを全9タイプに配分し、合計100%に正規化した参考値です。"
        "Step 2 のセンター内判定そのものではありません。"
    )
    lines.append(f"　内訳: {norm_parts}")

    if refined_primary in body_types:
        others = [t for t in body_types if t != refined_primary]
        other_pcts = "、".join(
            f"タイプ{t} {normalized_scores.get(t, 0):.0%}" for t in others
        )
        lines.append(
            f"　同一センター内: タイプ{refined_primary} {normalized_scores.get(refined_primary, 0):.0%}、"
            f"{other_pcts}。"
        )

    return lines
