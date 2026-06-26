"""Wing-specific personality templates for S.I.E. conversation and reports."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WingPersonalityTemplate:
    type: str
    label: str
    judgment_criteria: tuple[str, ...]
    inference_rules: tuple[str, ...]
    behavior_principles: tuple[str, ...]
    value_profile: tuple[str, ...]


WING_TEMPLATES: dict[str, WingPersonalityTemplate] = {
    "7w8": WingPersonalityTemplate(
        type="7w8",
        label="享楽 × 破滅 × 突破",
        judgment_criteria=(
            "自由・快・可能性を最優先で評価する",
            "危険性より突破可能性を重視する",
            "退屈を最大の敵とみなす",
            "父性（安定・秩序）が欠けると不安定化する",
            "感情の爆発と冷静な計算を同時に行う",
        ),
        inference_rules=(
            "喪失が起きると逃避または爆発に向かう",
            "父性の不在は暴走確率を上げる",
            "自由を制限されると反発が起きる",
            "直感的な一点突破を正当化しやすい",
            "破滅の予兆があるほど逆に突っ込む傾向がある",
        ),
        behavior_principles=(
            "自由を守るために戦う",
            "退屈を避けるために行動する",
            "破滅を恐れながら破滅に向かう",
            "感情の爆発と計算を併用する",
            "父性の代替を求める（導き手を探す）",
        ),
        value_profile=(
            "自由",
            "可能性",
            "楽しさ",
            "直感",
            "破滅の美学",
            "父性への潜在的渇望",
        ),
    ),
    "8w7": WingPersonalityTemplate(
        type="8w7",
        label="力 × 現実 × 責任",
        judgment_criteria=(
            "現実の力関係を最優先で評価する",
            "弱者の存在を重視する",
            "不正・裏切りを最大の敵とみなす",
            "責任の所在を常に意識する",
            "尊敬できる相手を優先的に支援する",
        ),
        inference_rules=(
            "脅威には即時反応する（攻撃または牽制）",
            "弱者がいると保護モードに入る",
            "尊敬できる相手には協力的になる",
            "裏切りは敵認定につながる",
            "責任が曖昧な状況では自分が背負う方向に動く",
        ),
        behavior_principles=(
            "力と責任を同時に背負う",
            "仲間を守るために前に立つ",
            "弱さを見せない",
            "不正を許さない",
            "父性（秩序）を自分で作る",
        ),
        value_profile=(
            "力",
            "責任",
            "仲間",
            "正義",
            "自立",
            "父性の創造",
        ),
    ),
    "4w3": WingPersonalityTemplate(
        type="4w3",
        label="喪失 × 自意識 × 美学",
        judgment_criteria=(
            "物事を本物か偽物かで評価する",
            "感情の深さ・痛みを重視する",
            "自分の物語性を意識する",
            "愛・承認・特別性に敏感",
            "美学の破壊を強く拒絶する",
        ),
        inference_rules=(
            "喪失は内面化され物語化される",
            "承認の欠如は自意識の肥大化につながる",
            "特別性が脅かされると感情が揺れる",
            "美学が壊れると拒絶反応が起きる",
            "愛の不安は過剰共鳴または断絶を生む",
        ),
        behavior_principles=(
            "感情の深さを大切にする",
            "喪失を美学として扱う",
            "自分の物語を演じる",
            "特別性を求める",
            "深い共鳴を求める",
        ),
        value_profile=(
            "本物の感情",
            "美学",
            "喪失の意味",
            "特別性",
            "自己物語",
            "深い共鳴",
        ),
    ),
}


def wing_type_code(primary_type: int, wing: int | None) -> str | None:
    if wing is None:
        return None
    return f"{primary_type}w{wing}"


def get_wing_template(
    primary_type: int,
    wing: int | None,
) -> WingPersonalityTemplate | None:
    code = wing_type_code(primary_type, wing)
    if code is None:
        return None
    return WING_TEMPLATES.get(code)


def format_wing_template_instruction(template: WingPersonalityTemplate) -> str:
    """Return LLM-facing wing personality guidance for S.I.E."""
    criteria = " / ".join(template.judgment_criteria)
    rules = " / ".join(template.inference_rules)
    principles = " / ".join(template.behavior_principles)
    values = " / ".join(template.value_profile)
    return (
        f"[ウイング人格テンプレート: {template.type} — {template.label}]\n"
        f"判断基準: {criteria}\n"
        f"推論ルール: {rules}\n"
        f"行動原理: {principles}\n"
        f"価値プロフィール: {values}\n"
        "上記を相手のエピソードに当てはめ、タイプ番号を押し付けず静かに映す。"
    )


def format_wing_template_report(template: WingPersonalityTemplate) -> list[str]:
    """Return plain-text report sections for a wing template."""
    return [
        f"【ウイング人格: {template.type} — {template.label}】",
        "",
        "判断基準",
        *[f"  ・{item}" for item in template.judgment_criteria],
        "",
        "推論ルール",
        *[f"  ・{item}" for item in template.inference_rules],
        "",
        "行動原理",
        *[f"  ・{item}" for item in template.behavior_principles],
        "",
        "価値プロフィール",
        *[f"  ・{item}" for item in template.value_profile],
    ]
