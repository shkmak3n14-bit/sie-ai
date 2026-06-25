"""Core fear/desire type questions (under-18 scenarios)."""

from __future__ import annotations

from sie.enneagram.questions import Question, _opts
from sie.enneagram.types import CENTER_TYPES, Center

CORE_TYPE_OPTION_WEIGHT = 2.5


def _tc_q(
    center: Center,
    num: int,
    text: str,
    category: str,
    options: tuple[tuple[str, int], ...],
) -> Question:
    prefix = {"body": "b", "heart": "h", "head": "k"}[center.value]
    return Question(
        id=f"tc_{prefix}_{num:02d}",
        text=text,
        category=category,
        options=_opts(
            *(
                (label, {str(type_num): CORE_TYPE_OPTION_WEIGHT})
                for label, type_num in options
            )
        ),
    )


TYPE_CORE_QUESTIONS_BODY: tuple[Question, ...] = (
    _tc_q(
        Center.BODY,
        1,
        "学生時代、「これだけは絶対に嫌」と感じた場面に近いのは？",
        "core_fear",
        (
            ("弱い・頼りないと見られること", 8),
            ("大切な関係が壊れて、対立が続くこと", 9),
            ("不完全・間違った人だと思われること", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        2,
        "心の底で、こうありたい・こう在りたいに近いのは？",
        "core_desire",
        (
            ("強く、自分の領域を守れる存在", 8),
            ("穏やかで、周りと調和している存在", 9),
            ("正しく、信頼できる存在", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        3,
        "理不尽なことを言われたとき、いちばん深い恐れは？",
        "core_fear",
        (
            ("コントロールを失い、尊重されないこと", 8),
            ("関係が壊れ、平和がなくなること", 9),
            ("自分が「悪い側」だと決めつけられること", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        4,
        "ストレスが限界のとき、自分を守る方法に近いのは？",
        "core_fear",
        (
            ("力で押し通す・境界を張る", 8),
            ("距離を取り、波風を立てない", 9),
            ("正しさを守り、改善しようとする", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        5,
        "グループで「自分はこう在りたい」と感じるのは？",
        "core_desire",
        (
            ("頼られる・守る側にいる", 8),
            ("みんなが無理なく過ごせる調整役", 9),
            ("ルールと公平さを守る人", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        6,
        "約束を破られたとき、いちばん刺さるのは？",
        "core_fear",
        (
            ("尊重されていないと感じる", 8),
            ("関係の亀裂・不和", 9),
            ("正しくない・不公平だという感覚", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        7,
        "将来、これだけは避けたい状態に近いのは？",
        "core_fear",
        (
            ("弱さを見せて支配されること", 8),
            ("争い続けて疲弊すること", 9),
            ("道徳的に「ダメな人」になること", 1),
        ),
    ),
    _tc_q(
        Center.BODY,
        8,
        "自分にとって「正しい生き方」に近いのは？",
        "core_desire",
        (
            ("率直に真実を見て、力強く生きる", 8),
            ("穏やかに、みんなと調和して生きる", 9),
            ("誠実に、善く正しく生きる", 1),
        ),
    ),
)

TYPE_CORE_QUESTIONS_HEART: tuple[Question, ...] = (
    _tc_q(
        Center.HEART,
        1,
        "「これだけは絶対に嫌」と感じやすいのは？",
        "core_fear",
        (
            ("必要とされず、愛されないこと", 2),
            ("価値のない・認められない存在になること", 3),
            ("自分らしさがなく、普通・凡庸だと言われること", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        2,
        "心の底で求めているものに近いのは？",
        "core_desire",
        (
            ("愛され、必要とされること", 2),
            ("認められ、価値ある存在であること", 3),
            ("自分らしさ・意味のある存在であること", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        3,
        "友達に置いていかれたとき、いちばん深い恐れは？",
        "core_fear",
        (
            ("本当の自分では愛されないこと", 2),
            ("価値が下がり、見下されること", 3),
            ("特別なつながりを失うこと", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        4,
        "褒められて、いちばん「自分の本音」に響くのは？",
        "core_desire",
        (
            ("「助けてくれてありがとう」", 2),
            ("「さすが、結果が出ているね」", 3),
            ("「あなたにしかない感性だね」", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        5,
        "SNSやクラスで、自分をどう見られたい？",
        "core_desire",
        (
            ("温かく、頼られる人", 2),
            ("有能で、成功している人", 3),
            ("独自の世界観を持つ特別な人", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        6,
        "努力しても報われないとき、恐れに近いのは？",
        "core_fear",
        (
            ("与えても愛されないこと", 2),
            ("成果がなく、価値がないと思われること", 3),
            ("本物の自分が伝わらないこと", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        7,
        "親友とケンカしたあと、いちばん怖いのは？",
        "core_fear",
        (
            ("関係が終わり、必要とされなくなること", 2),
            ("評価が下がり、立場が悪くなること", 3),
            ("深い理解を失い、一人になること", 4),
        ),
    ),
    _tc_q(
        Center.HEART,
        8,
        "進路や部活を選ぶ基準、本音に近いのは？",
        "core_desire",
        (
            ("人の役に立てる・感謝される", 2),
            ("成果・評価が見える", 3),
            ("自分の感性・意味が生きる", 4),
        ),
    ),
)

TYPE_CORE_QUESTIONS_HEAD: tuple[Question, ...] = (
    _tc_q(
        Center.HEAD,
        1,
        "「これだけは絶対に嫌」と感じやすいのは？",
        "core_fear",
        (
            ("無能で、世界を理解できないこと", 5),
            ("支えがなく、危険にさらされること", 6),
            ("自由を失い、苦しみに閉じ込められること", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        2,
        "心の底で求めているものに近いのは？",
        "core_desire",
        (
            ("有能で、理解している存在であること", 5),
            ("安全で、支援されていること", 6),
            ("自由で、満たされていること", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        3,
        "初対面の場で、いちばん強い不安は？",
        "core_fear",
        (
            ("対応できず、無能だと思われること", 5),
            ("信頼できず、最悪のことが起きること", 6),
            ("退屈・束縛・つまらない未来になること", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        4,
        "テスト前に頭から離れない恐れに近いのは？",
        "core_fear",
        (
            ("理解不足で、対応できないこと", 5),
            ("準備不足で、想定外の失敗をすること", 6),
            ("失敗が続き、楽しさや自由がなくなること", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        5,
        "一人の時間、本音に近い過ごし方は？",
        "core_desire",
        (
            ("調べ物・読書で理解を深める", 5),
            ("計画を立て、安心できる状態を作る", 6),
            ("好きなこと・新しい可能性を探す", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        6,
        "誰かに頼り切られたとき、内心どう感じる？",
        "core_fear",
        (
            ("エネルギーが削られ、距離を取りたい", 5),
            ("責任が重く、失敗が怖い", 6),
            ("自由が減り、退屈・束縛を感じる", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        7,
        "将来が不安な夜、いちばん長く続く思考は？",
        "core_fear",
        (
            ("自分は十分でない・分かっていない", 5),
            ("最悪の展開・信頼できない人", 6),
            ("選択肢が狭まり、楽しみがなくなる", 7),
        ),
    ),
    _tc_q(
        Center.HEAD,
        8,
        "自分にとって「安心できる状態」に近いのは？",
        "core_desire",
        (
            ("十分な知識と、一人の時間がある", 5),
            ("信頼できる人・明確なルールがある", 6),
            ("自由と、楽しみの選択肢がある", 7),
        ),
    ),
)

TYPE_CORE_QUESTIONS_BY_CENTER: dict[Center, tuple[Question, ...]] = {
    Center.BODY: TYPE_CORE_QUESTIONS_BODY,
    Center.HEART: TYPE_CORE_QUESTIONS_HEART,
    Center.HEAD: TYPE_CORE_QUESTIONS_HEAD,
}


def get_type_core_questions(center: Center) -> tuple[Question, ...]:
    return TYPE_CORE_QUESTIONS_BY_CENTER[center]
