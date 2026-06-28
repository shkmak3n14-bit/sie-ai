"""Enneagram type metadata and center definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Center(str, Enum):
    BODY = "body"
    HEART = "heart"
    HEAD = "head"


CENTER_TYPES: dict[Center, tuple[int, ...]] = {
    Center.BODY: (8, 9, 1),
    Center.HEART: (2, 3, 4),
    Center.HEAD: (5, 6, 7),
}

TYPE_TO_CENTER: dict[int, Center] = {
    type_num: center
    for center, types in CENTER_TYPES.items()
    for type_num in types
}

STRESS_PATTERN: dict[int, int] = {
    1: 4, 2: 8, 3: 9, 4: 2, 5: 7, 6: 3, 7: 1, 8: 5, 9: 6,
}

GROWTH_PATTERN: dict[int, int] = {
    1: 7, 2: 4, 3: 6, 4: 1, 5: 8, 6: 9, 7: 5, 8: 2, 9: 3,
}


def wing_types(primary_type: int) -> tuple[int, int]:
    """Return the two adjacent wing type numbers."""
    if primary_type == 1:
        return 9, 2
    if primary_type == 9:
        return 8, 1
    return primary_type - 1, primary_type + 1


@dataclass(frozen=True)
class TypeInfo:
    number: int
    name: str
    center: Center
    summary: str
    strengths: tuple[str, ...]
    blind_spots: tuple[str, ...]
    core_fear: str
    core_desire: str
    communication_style: str
    conflict_pattern: str
    relationship_needs: tuple[str, ...]
    childhood_wound: str


TYPE_INFO: dict[int, TypeInfo] = {
    1: TypeInfo(
        number=1,
        name="タイプ1：改革する人",
        center=Center.BODY,
        summary="正しさと改善への強い志向を持ち、自分にも他人にも高い基準を求めるタイプ。",
        strengths=("責任感", "誠実さ", "改善への情熱", "一貫性"),
        blind_spots=("完璧主義", "自己批判", "柔軟性の不足", "怒りの抑圧"),
        core_fear="不完全であること、悪い人間であること",
        core_desire="正しくあり、善であること",
        communication_style="論理的で明確。改善点を指摘しやすいが、意図は建設的。",
        conflict_pattern="正しさを守ろうとして硬くなり、相手の怠慢に苛立つ。",
        relationship_needs=("誠実さ", "約束の履行", "敬意", "秩序"),
        childhood_wound="愛は正しく振る舞ったときにもらえる、という信念",
    ),
    2: TypeInfo(
        number=2,
        name="タイプ2：助ける人",
        center=Center.HEART,
        summary="他者のニーズに敏感で、与えることで愛されていると感じようとするタイプ。",
        strengths=("共感力", "支援力", "温かさ", "人間関係の構築力"),
        blind_spots=("自分のニーズの軽視", "見返りの期待", "境界線の曖昧さ"),
        core_fear="自分自身では愛されないこと",
        core_desire="愛され、必要とされること",
        communication_style="温かく気配りが行き届く。相手の状態を先に読み取る。",
        conflict_pattern="拒絶を恐れて直接言わず、与え続けた後に失望する。",
        relationship_needs=("感謝", "つながり", "相互のケア", "特別感"),
        childhood_wound="自分の欲求より他者を優先しないと価値がない、という信念",
    ),
    3: TypeInfo(
        number=3,
        name="タイプ3：達成する人",
        center=Center.HEART,
        summary="成功と効率を重視し、成果で自己価値を測る適応力の高いタイプ。",
        strengths=("実行力", "適応力", "目標達成", "カリスマ性"),
        blind_spots=("本音の軽視", "休息の不足", "評価への依存"),
        core_fear="価値のない存在になること",
        core_desire="価値ある存在であり、認められること",
        communication_style="簡潔で前向き。成果や可能性を強調する。",
        conflict_pattern="失敗や非効率に苛立ち、感情より結果を優先する。",
        relationship_needs=("承認", "共に成長する感覚", "効率的な関わり"),
        childhood_wound="成果を出さないと愛されない、という信念",
    ),
    4: TypeInfo(
        number=4,
        name="タイプ4：個性を求める人",
        center=Center.HEART,
        summary="深い感情と独自性を大切にし、意味のあるつながりを求めるタイプ。",
        strengths=("感受性", "創造性", "深い共感", "本物志向"),
        blind_spots=("比較による苦しみ", "気分の起伏", "欠如への焦点"),
        core_fear="自分には特別な意味やアイデンティティがないこと",
        core_desire="自分らしさを見出し、意味のある存在になること",
        communication_style="詩的で個人的。感情の深さを大切にする。",
        conflict_pattern="誤解されたと感じて距離を取る、または感情が溢れる。",
        relationship_needs=("理解", "深いつながり", "自分だけの特別さ", "誠実な共感"),
        childhood_wound="本当の自分は欠けている、という信念",
    ),
    5: TypeInfo(
        number=5,
        name="タイプ5：調べる人",
        center=Center.HEAD,
        summary="知識と内省を通じて世界を理解し、エネルギーとプライバシーを守るタイプ。",
        strengths=("分析力", "客観性", "集中力", "独創的な洞察"),
        blind_spots=("孤立", "感情の切り離し", "行動の遅れ", "過剰な観察"),
        core_fear="無能で、支援も世界もないこと",
        core_desire="有能であり、世界を理解すること",
        communication_style="簡潔で論理的。必要最小限の情報を共有する。",
        conflict_pattern="圧倒されると引きこもり、感情より分析で距離を取る。",
        relationship_needs=("個人的な時間", "知的な刺激", "干渉の少なさ", "信頼"),
        childhood_wound="世界は要求が多すぎる、自分のリソースは限られている、という信念",
    ),
    6: TypeInfo(
        number=6,
        name="タイプ6：忠実な人",
        center=Center.HEAD,
        summary="安全と信頼を基盤に、リスクを見極めながら所属と支援を求めるタイプ。",
        strengths=("忠誠心", "責任感", "危機対応力", "チームワーク"),
        blind_spots=("不安の増幅", "決断の先延ばし", "権威への揺れ"),
        core_fear="支えなく、危険にさらされること",
        core_desire="安全で、支援されていること",
        communication_style="慎重で具体的。確認質問やシナリオ検討が多い。",
        conflict_pattern="不信感が高まると防御的になり、最悪のシナリオを想定する。",
        relationship_needs=("信頼", "一貫性", "安心感", "明確な約束"),
        childhood_wound="世界は危うく、頼れるものは限られている、という信念",
    ),
    7: TypeInfo(
        number=7,
        name="タイプ7：熱中する人",
        center=Center.HEAD,
        summary="可能性と楽しさを追い、苦痛から距離を取りながら前向きに拡散するタイプ。",
        strengths=("楽観性", "発想力", "行動力", "困難を軽やかにする力"),
        blind_spots=("逃避", "集中の散漫", "深い感情の回避", "過剰な約束"),
        core_fear="閉じ込められ、苦痛や退屈に耐えられないこと",
        core_desire="満たされ、幸せであること",
        communication_style="明るくテンポが速い。アイデアや選択肢を次々提示する。",
        conflict_pattern="重い話題を避け、冗談や話題転換で距離を取る。",
        relationship_needs=("自由", "楽しさ", "新しい刺激", "前向きな空気"),
        childhood_wound="苦痛は避けるべきで、満たされないと耐えられない、という信念",
    ),
    8: TypeInfo(
        number=8,
        name="タイプ8：挑戦する人",
        center=Center.BODY,
        summary="力強さと正義感で自分の領域を守り、弱さを見せずに主導するタイプ。",
        strengths=("決断力", "保護力", "率直さ", "行動力"),
        blind_spots=("支配", "脆弱性の否認", "過剰な対立"),
        core_fear="弱さや支配されること",
        core_desire="自分の人生をコントロールし、影響力を持つこと",
        communication_style="直接的で力強い。本音を隠さず、即決する。",
        conflict_pattern="挑発に対して力で応じ、コントロールを失うと爆発する。",
        relationship_needs=("正直さ", "自立", "忠誠", "対等な関係"),
        childhood_wound="弱さを見せると傷つけられる、という信念",
    ),
    9: TypeInfo(
        number=9,
        name="タイプ9：平和を求める人",
        center=Center.BODY,
        summary="調和と安定を重視し、対立を避けながら全体の平和を保とうとするタイプ。",
        strengths=("穏やかさ", "受容力", "調停力", "忍耐"),
        blind_spots=("自己主張の遅れ", "優先順位の曖昧さ", "受動性"),
        core_fear="分断や喪失、関係の断絶",
        core_desire="内的・外的な平和と調和",
        communication_style="穏やかで聞き上手。相手の意見を取り込みやすい。",
        conflict_pattern="対立を避けて黙り込み、後から距離を取るか突然固執する。",
        relationship_needs=("調和", "穏やかな時間", "受容", "急かされないペース"),
        childhood_wound="自分の意見は重要ではない、平和を乱すな、という信念",
    ),
}


def get_type_info(type_number: int) -> TypeInfo:
    return TYPE_INFO[type_number]
