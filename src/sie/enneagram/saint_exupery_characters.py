"""Saint-Exupéry / Le Petit Prince character model — separating Type 3 and Type 4."""

from __future__ import annotations

from dataclasses import dataclass

from sie.enneagram.wing_templates import wing_type_code


@dataclass(frozen=True)
class CharacterArchetype:
    key: str
    name: str
    enneagram_type: str
    subtype: str
    core_motivation: str
    core_fear: str
    core_desire: str
    patterns: tuple[str, ...]
    narrative_role: str
    relation_to_author: str


CHARACTER_ARCHETYPES: dict[str, CharacterArchetype] = {
    "prince": CharacterArchetype(
        key="prince",
        name="王子さま",
        enneagram_type="4",
        subtype="4w3（作者の内的核を反映）",
        core_motivation="唯一性と本物の愛を求める",
        core_fear="特別な存在でなくなること、愛を失うこと",
        core_desire="深く理解され、唯一の存在として愛されること",
        patterns=(
            "喪失を美化する",
            "感情を象徴化して語る",
            "愛しているのに距離を取る",
            "世界を“感情の風景”として認識する",
        ),
        narrative_role="作者の“内なる子ども”としての4の純粋性を体現する存在",
        relation_to_author="サン＝テグジュペリ自身の内面（4の核）を象徴",
    ),
    "rose": CharacterArchetype(
        key="rose",
        name="バラ",
        enneagram_type="4（象徴的存在）",
        subtype="4の欲求の象徴化",
        core_motivation="唯一無二の愛を求める",
        core_fear="自分が特別でないこと",
        core_desire="選ばれた存在であること",
        patterns=(
            "愛情を試す",
            "不安からの駆け引き",
            "特別扱いを求める",
            "存在そのものが象徴的意味を持つ",
        ),
        narrative_role="“唯一性への執着”を象徴する存在",
        relation_to_author="作者が求め続けた“唯一の愛”の象徴",
    ),
    "fox": CharacterArchetype(
        key="fox",
        name="キツネ",
        enneagram_type="1 or 9（4の成長方向）",
        subtype="4の統合先の象徴",
        core_motivation="関係の本質を理解し、秩序と意味を与える",
        core_fear="関係が表面的で終わること",
        core_desire="“絆”が本物であること",
        patterns=(
            "関係の本質を言語化する",
            "感情を整理し、意味づける",
            "4の混乱に秩序を与える",
            "“手なづける”＝関係の本質を教える",
        ),
        narrative_role="4が成長するための“関係の真理”を教える存在",
        relation_to_author="作者が人生で求め続けた“関係の本質”の象徴",
    ),
    "pilot": CharacterArchetype(
        key="pilot",
        name="飛行士",
        enneagram_type="3",
        subtype="3w4（大人の仮面）",
        core_motivation="社会的に通用する役割を果たすこと",
        core_fear="無価値であること、役割を失うこと",
        core_desire="有能であり、認められること",
        patterns=(
            "感情より役割を優先する",
            "理解されない痛みを隠す",
            "“大人”として振る舞う",
            "内面の4を守るために外側を3で固める",
        ),
        narrative_role="作者の“社会的仮面（3）”を象徴する存在",
        relation_to_author="サン＝テグジュペリ自身の外側の人格（大人・英雄・適応者）",
    ),
}

# Which inner parts apply per wing code (3と4の分離モデル).
_CHARACTERS_BY_WING_CODE: dict[str, tuple[str, ...]] = {
    "4w3": ("prince", "rose", "fox", "pilot"),
    "4w5": ("prince", "rose", "fox"),
    "3w4": ("pilot", "prince", "fox"),
}

_FALLBACK_BY_PRIMARY: dict[int, tuple[str, ...]] = {
    4: ("prince", "rose", "fox"),
    3: ("pilot",),
}


def get_saint_exupery_characters(
    primary_type: int,
    wing: int | None,
) -> tuple[CharacterArchetype, ...]:
    """Return applicable character archetypes for Type 3 / 4 profiles."""
    if primary_type not in (3, 4):
        return ()
    code = wing_type_code(primary_type, wing)
    keys = _CHARACTERS_BY_WING_CODE.get(code or "", _FALLBACK_BY_PRIMARY[primary_type])
    return tuple(CHARACTER_ARCHETYPES[k] for k in keys if k in CHARACTER_ARCHETYPES)


def format_character_instruction(characters: tuple[CharacterArchetype, ...]) -> str:
    """Return LLM-facing character model guidance."""
    if not characters:
        return ""
    lines = [
        "[星の王子さま模型 — タイプ3と4の分離（サン＝テグジュペリ）]",
        "内面の4（王子・バラ）と外面の3（飛行士）、成長のキツネを区別して映す。",
        "",
    ]
    for char in characters:
        lines.append(f"■ {char.name}（{char.enneagram_type} / {char.subtype}）")
        lines.append(f"  動機: {char.core_motivation}")
        lines.append(f"  恐れ: {char.core_fear}")
        lines.append(f"  欲求: {char.core_desire}")
        lines.append(f"  パターン: {' / '.join(char.patterns)}")
        lines.append(f"  物語上の役割: {char.narrative_role}")
        lines.append(f"  作者との関係: {char.relation_to_author}")
        lines.append("")
    lines.append(
        "キャラクター名やタイプ番号を押し付けず、"
        "内面の4と外面の3がどう分かれているかを相手の言葉で静かに映す。"
    )
    return "\n".join(lines)


def format_character_report(characters: tuple[CharacterArchetype, ...]) -> list[str]:
    """Return plain-text report sections."""
    if not characters:
        return []
    lines = [
        "【星の王子さま模型 — タイプ3と4の分離】",
        "",
    ]
    for char in characters:
        lines.extend(
            [
                f"{char.name}（{char.enneagram_type} / {char.subtype}）",
                f"  動機: {char.core_motivation}",
                f"  恐れ: {char.core_fear}",
                f"  欲求: {char.core_desire}",
                "  パターン:",
                *[f"    ・{p}" for p in char.patterns],
                f"  物語上の役割: {char.narrative_role}",
                f"  作者との関係: {char.relation_to_author}",
                "",
            ]
        )
    return lines


def format_character_html(characters: tuple[CharacterArchetype, ...]) -> str:
    """Return HTML fragment for character sections."""
    if not characters:
        return ""
    parts = ['<h3>星の王子さま模型 — タイプ3と4の分離</h3>']
    for char in characters:
        patterns = "".join(f"<li>{p}</li>" for p in char.patterns)
        parts.append(f"""\
<h4>{char.name}（{char.enneagram_type} / {char.subtype}）</h4>
<p><strong>動機:</strong> {char.core_motivation}<br>
<strong>恐れ:</strong> {char.core_fear}<br>
<strong>欲求:</strong> {char.core_desire}</p>
<p><strong>パターン</strong></p>
<ul>{patterns}</ul>
<p><strong>物語上の役割:</strong> {char.narrative_role}<br>
<strong>作者との関係:</strong> {char.relation_to_author}</p>""")
    return "\n".join(parts)
