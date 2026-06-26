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
    model_name: str | None = None
    decision_criteria: dict[str, str] | None = None
    inference_rules_map: dict[str, str] | None = None
    behavioral_principles: dict[str, str] | None = None
    value_profile_structured: dict[str, tuple[str, ...]] | None = None


_VALUE_PROFILE_LABELS: dict[str, str] = {
    "likes": "好む",
    "dislikes": "嫌う",
    "respects": "尊敬する",
    "contempts": "軽蔑する",
}


_7W6_DECISION_CRITERIA: dict[str, str] = {
    "stimulus_priority": "退屈より刺激を優先する。刺激が強いほど価値が高いと判断する。",
    "risk_reinterpretation": "危険を快楽・高揚・勝負の場として肯定的に再定義する。",
    "effort_selection": "興味対象には全力で努力するが、義務や退屈は切り捨てる。",
    "anxiety_management": "不安を刺激で上書きできるかどうかで行動を決定する。",
    "loyalty_ranking": "自分が相手にとって何番目かを常に計測し、行動強度を変える。",
    "optimism_bias": "押せばなんとかなるという期待値を高く見積もる。",
    "visibility_safety_conflict": "目立ちたいが安全も求めるため、結果として地味な選択をしがち。",
}

_7W6_INFERENCE_RULES: dict[str, str] = {
    "stimulus_equals_value": "刺激が強いほど正しい選択と推論する。",
    "anxiety_denial": "不安は直視する対象ではなく、刺激で上書きする対象と解釈する。",
    "rapid_rationalization": "自分の行動を正当化する論理を高速生成する。",
    "reading_between_lines": "相手の裏・ルールの抜け道を常に探索する。",
    "position_inference": "他者の言動から自分の順位を推測し、行動に反映する。",
    "overestimated_expectation": "未来の成功確率を楽観的に見積もる。",
    "awareness_of_ruin": "楽しさに溺れると破滅することを理解しているが、それでも価値があると判断する。",
}

_7W6_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "full_power_on_interest": "興味対象には異常な集中力を発揮する。",
    "abandon_duties": "楽しいことが見つかると義務や責任を後回しにする。",
    "anxiety_overwrite_action": "不安を感じると刺激の強い行動で上書きしようとする。",
    "overpush": "押せば通るという楽観で限界を超えて押し続ける。",
    "escape_and_betrayal_conditions": "動機が浅い場合、飽き・逃避・裏切りが発生しやすい。",
    "pleasurable_courage": "張った目が裏目でも受け入れる覚悟がある（恐怖否認 × 忠誠）。",
    "suggestibility": "他者の言葉に影響されやすい。",
    "visibility_conflict_behavior": "目立ちたいが安全志向が働き、地味な選択をしがち。",
}

_7W6_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "likes": (
        "刺激・スリル・高揚感",
        "勝負・逆転・賭け",
        "自由・選択肢の多さ",
        "戦略・裏をかく知性",
        "スピード感・勢い",
        "希望・楽観・未来志向",
        "仲間・忠誠・順位の安定",
    ),
    "dislikes": (
        "退屈・停滞",
        "束縛・管理",
        "痛み・責任・義務",
        "不安を直視すること",
        "単調な努力",
        "自分の順位が低い状態",
        "押しても通らない状況",
    ),
    "respects": (
        "命を賭ける価値のある勝負",
        "努力の末の一撃",
        "自分の選択に責任を取る覚悟",
        "刺激のある人生",
        "裏を読んで勝つ知性",
    ),
    "contempts": (
        "退屈な人生",
        "安全のための妥協",
        "努力しないで文句を言う態度",
        "自分の恐怖に飲まれること",
    ),
}


WING_TEMPLATES: dict[str, WingPersonalityTemplate] = {
    "2w1": WingPersonalityTemplate(
        type="2w1",
        label="献身 × 義務 × 過剰な救済欲求",
        judgment_criteria=(
            "他者のニーズを最優先で評価する",
            "『助けるべき相手』を中心に世界を認識する",
            "愛・承認・必要とされることを強く求める",
            "倫理より『救うこと』を優先する傾向がある",
            "自分が助けなければならないという義務感で判断する",
        ),
        inference_rules=(
            "喪失の恐れが強まるほど、救済行動が過剰化する",
            "助けを拒む者・妨害する者を敵とみなす",
            "力を持つ者に近づき、力を得ようとする（救うため）",
            "使命感（1の要素）が強まると『自分がやらねば』が暴走する",
            "ストレス下では8的攻撃性が正当化される（救うための暴力）",
            "愛する者を守るためなら倫理を曲げても良いと推論する",
            "『相手を助ける＝自分の存在価値』という構造で行動を正当化する",
        ),
        behavior_principles=(
            "他者を救うことを最優先に行動する",
            "愛する者を守るために力を求める",
            "救済のために自己犠牲をいとわない",
            "妨害者を排除しようとする（正義感の暴走）",
            "助ける行為を義務化し、自分を追い込む",
            "愛・承認を得るために過剰に尽くす",
            "『救うための暴力』を正当化しやすい",
        ),
        value_profile=(
            "愛と承認",
            "献身と救済",
            "義務と責任（1の要素）",
            "力の獲得（救うため）",
            "倫理よりも『守るべき者』の幸福",
            "喪失の回避",
            "忠誠と信頼",
        ),
    ),
    "7w6": WingPersonalityTemplate(
        type="7w6",
        label="刺激 × 楽観 × 忠誠",
        model_name="Fukumoto-Style_7w6",
        judgment_criteria=tuple(_7W6_DECISION_CRITERIA.values()),
        inference_rules=tuple(_7W6_INFERENCE_RULES.values()),
        behavior_principles=tuple(_7W6_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            f"{_VALUE_PROFILE_LABELS[key]}: {' / '.join(items)}"
            for key, items in _7W6_VALUE_PROFILE.items()
        ),
        decision_criteria=_7W6_DECISION_CRITERIA,
        inference_rules_map=_7W6_INFERENCE_RULES,
        behavioral_principles=_7W6_BEHAVIORAL_PRINCIPLES,
        value_profile_structured=_7W6_VALUE_PROFILE,
    ),
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


def _template_header(template: WingPersonalityTemplate) -> str:
    if template.model_name:
        return f"{template.type} — {template.label}（{template.model_name}）"
    return f"{template.type} — {template.label}"


def _format_dict_section(title: str, items: dict[str, str]) -> str:
    lines = [f"{title}:"]
    for value in items.values():
        lines.append(f"  ・{value}")
    return "\n".join(lines)


def _format_structured_values(values: dict[str, tuple[str, ...]]) -> str:
    lines = ["価値プロフィール:"]
    for key, items in values.items():
        label = _VALUE_PROFILE_LABELS.get(key, key)
        lines.append(f"  {label}: {' / '.join(items)}")
    return "\n".join(lines)


def format_wing_template_instruction(template: WingPersonalityTemplate) -> str:
    """Return LLM-facing wing personality guidance for S.I.E."""
    header = _template_header(template)
    if template.decision_criteria:
        criteria_block = _format_dict_section("判断基準", template.decision_criteria)
        rules_block = _format_dict_section(
            "推論ルール",
            template.inference_rules_map or {},
        )
        principles_block = _format_dict_section(
            "行動原理",
            template.behavioral_principles or {},
        )
        values_block = _format_structured_values(template.value_profile_structured or {})
        body = "\n".join(
            part for part in (criteria_block, rules_block, principles_block, values_block) if part
        )
    else:
        body = (
            f"判断基準: {' / '.join(template.judgment_criteria)}\n"
            f"推論ルール: {' / '.join(template.inference_rules)}\n"
            f"行動原理: {' / '.join(template.behavior_principles)}\n"
            f"価値プロフィール: {' / '.join(template.value_profile)}"
        )
    return (
        f"[ウイング人格テンプレート: {header}]\n"
        f"{body}\n"
        "上記を相手のエピソードに当てはめ、タイプ番号を押し付けず静かに映す。"
    )


def _report_dict_section(title: str, items: dict[str, str]) -> list[str]:
    return [title, *[f"  ・{value}" for value in items.values()], ""]


def _report_structured_values(values: dict[str, tuple[str, ...]]) -> list[str]:
    lines = ["価値プロフィール", ""]
    for key, items in values.items():
        label = _VALUE_PROFILE_LABELS.get(key, key)
        lines.append(label)
        lines.extend(f"  ・{item}" for item in items)
        lines.append("")
    return lines


def format_wing_template_report(template: WingPersonalityTemplate) -> list[str]:
    """Return plain-text report sections for a wing template."""
    lines = [f"【ウイング人格: {_template_header(template)}】", ""]
    if template.decision_criteria:
        lines.extend(_report_dict_section("判断基準", template.decision_criteria))
        lines.extend(
            _report_dict_section("推論ルール", template.inference_rules_map or {})
        )
        lines.extend(
            _report_dict_section("行動原理", template.behavioral_principles or {})
        )
        lines.extend(_report_structured_values(template.value_profile_structured or {}))
    else:
        lines.extend(
            [
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
        )
    return lines


def format_wing_template_html(template: WingPersonalityTemplate) -> str:
    """Return HTML fragment for a wing template section."""

    def lis(items: tuple[str, ...]) -> str:
        return "".join(f"<li>{item}</li>" for item in items)

    def lis_dict(items: dict[str, str]) -> str:
        return "".join(f"<li>{value}</li>" for value in items.values())

    header = _template_header(template)
    if template.decision_criteria:
        values_html = ""
        for key, items in (template.value_profile_structured or {}).items():
            label = _VALUE_PROFILE_LABELS.get(key, key)
            values_html += f"<h5>{label}</h5><ul>{lis(items)}</ul>"
        return f"""\
  <h3>ウイング人格: {header}</h3>
  <h4>判断基準</h4>
  <ul>{lis_dict(template.decision_criteria)}</ul>
  <h4>推論ルール</h4>
  <ul>{lis_dict(template.inference_rules_map or {})}</ul>
  <h4>行動原理</h4>
  <ul>{lis_dict(template.behavioral_principles or {})}</ul>
  <h4>価値プロフィール</h4>
  {values_html}"""

    return f"""\
  <h3>ウイング人格: {header}</h3>
  <h4>判断基準</h4>
  <ul>{lis(template.judgment_criteria)}</ul>
  <h4>推論ルール</h4>
  <ul>{lis(template.inference_rules)}</ul>
  <h4>行動原理</h4>
  <ul>{lis(template.behavior_principles)}</ul>
  <h4>価値プロフィール</h4>
  <ul>{lis(template.value_profile)}</ul>"""
