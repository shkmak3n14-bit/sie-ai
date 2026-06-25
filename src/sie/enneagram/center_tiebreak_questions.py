"""Tie-breaker center questions for borderline body / heart / head scores."""

from __future__ import annotations

from sie.enneagram.questions import Question, _opts
from sie.enneagram.types import Center

TIEBREAK_OPTION_WEIGHT = 3.0

_CENTER_ORDER = (Center.BODY, Center.HEART, Center.HEAD)


def normalize_center_pair(a: Center, b: Center) -> tuple[Center, Center]:
    """Return pair in body → heart → head order."""
    order = {c: i for i, c in enumerate(_CENTER_ORDER)}
    if order[a] > order[b]:
        return (b, a)
    return (a, b)


def _tb_q(
    pair_key: str,
    num: int,
    text: str,
    first: Center,
    first_text: str,
    second: Center,
    second_text: str,
) -> Question:
    return Question(
        id=f"ct_{pair_key}_{num:02d}",
        text=text,
        category="center_tiebreak",
        options=_opts(
            (first_text, {first.value: TIEBREAK_OPTION_WEIGHT}),
            (second_text, {second.value: TIEBREAK_OPTION_WEIGHT}),
        ),
    )


# body vs heart — 5 questions
_BODY_HEART: tuple[Question, ...] = (
    _tb_q(
        "bh", 1,
        "先生に「もっと周りを見なさい」と言われた直後、心の声に近いのは？",
        Center.BODY, "「自分は悪くない。理不尽だ」と腹が立つ",
        Center.HEART, "「嫌われたかも。みんなの前で恥ずかしい」",
    ),
    _tb_q(
        "bh", 2,
        "親友が、あなた抜きで他の友達と遊んでいるのを見ました。最初の感覚は？",
        Center.BODY, "「裏切られた」と感じ、距離を取りたくなる",
        Center.HEART, "「自分は必要ないのか」と寂しく、傷つく",
    ),
    _tb_q(
        "bh", 3,
        "グループワークで自分の案が無視されました。あなたは？",
        Center.BODY, "「聞いてない」と感じ、はっきり言い返す",
        Center.HEART, "「嫌われた？」と不安になり、様子をうかがう",
    ),
    _tb_q(
        "bh", 4,
        "親に「兄（姉）の方ができる」と言われた。いちばん残るのは？",
        Center.BODY, "悔しさ・反発——「比べるな」",
        Center.HEART, "「自分は足りない」と落ち込み、認めてほしくなる",
    ),
    _tb_q(
        "bh", 5,
        "教室で大声で名前を呼ばれ、答えを間違えました。その後ずっと残るのは？",
        Center.BODY, "体のこわばり・言い返しそうになった記憶",
        Center.HEART, "「バカにされた」「どう見られているか」の記憶",
    ),
)

# heart vs head — 5 questions
_HEART_HEAD: tuple[Question, ...] = (
    _tb_q(
        "hh", 1,
        "知らないクラスの子たちに囲まれ、話しかけられました。最初の不安は？",
        Center.HEART, "「どう思われるか・変に思われないか」",
        Center.HEAD, "「何を聞かれるか・どう答えるか・最悪どうなるか」",
    ),
    _tb_q(
        "hh", 2,
        "親友が急に返事をしなくなりました。考えが続くのは？",
        Center.HEART, "「怒ってる？もう仲良くない？」",
        Center.HEAD, "「忙しいのか・何かあったのか・どう確認するか」",
    ),
    _tb_q(
        "hh", 3,
        "進路選択で、同じくらい魅力的な2つの道があります。決め手は？",
        Center.HEART, "大切な人からどう見られるか・誇れるか",
        Center.HEAD, "リスク・将来性・情報が揃っているか",
    ),
    _tb_q(
        "hh", 4,
        "自分についてうわさが流れています。頭から離れないのは？",
        Center.HEART, "「みんなにどう思われているか」",
        Center.HEAD, "「本当かどうか・誰が言ったか・どう対処するか」",
    ),
    _tb_q(
        "hh", 5,
        "文化祭の出し物を決める会議で意見が割れました。あなたの関心は？",
        Center.HEART, "みんなが楽しめるか・仲良く進められるか",
        Center.HEAD, "失敗しないか・準備は足りるか・何が起きうるか",
    ),
)

# head vs body — 5 questions
_HEAD_BODY: tuple[Question, ...] = (
    _tb_q(
        "hb", 1,
        "急に予定が変更され、今日の予定が全部崩れました。最初の反応は？",
        Center.HEAD, "頭の中で新しい予定を組み直し始める",
        Center.BODY, "イライラする・「勝手に変えるな」と感じる",
    ),
    _tb_q(
        "hb", 2,
        "ケンカの直前、あなたの内側で起きているのは？",
        Center.HEAD, "相手の言動を分析し、言い返す文句を考える",
        Center.BODY, "体が熱くなり、今すぐ言いたくなる",
    ),
    _tb_q(
        "hb", 3,
        "夜道を一人で歩いていて、不気味な場所に入りました。最初の反応は？",
        Center.HEAD, "「最悪こうなったら…」とシナリオを想像する",
        Center.BODY, "足が速くなる・周囲を見る・直感で距離を取る",
    ),
    _tb_q(
        "hb", 4,
        "大事な発表の結果を待っています。待っている間の状態は？",
        Center.HEAD, "合格/不合格それぞれの場合を何度も頭の中で再生する",
        Center.BODY, "落ち着かない・足を動かす・体が張る",
    ),
    _tb_q(
        "hb", 5,
        "時間がなく、すぐ決断しなければならない場面。あなたは？",
        Center.HEAD, "もう少し情報が欲しいと感じ、考える",
        Center.BODY, "直感で「これだ」と動く",
    ),
)

def get_center_tiebreak_questions(pair: tuple[Center, Center]) -> tuple[Question, ...]:
    """Return 5 tie-breaker questions for the given center pair."""
    a, b = normalize_center_pair(pair[0], pair[1])
    mapping: dict[tuple[Center, Center], tuple[Question, ...]] = {
        (Center.BODY, Center.HEART): _BODY_HEART,
        (Center.HEART, Center.HEAD): _HEART_HEAD,
        (Center.BODY, Center.HEAD): _HEAD_BODY,
    }
    questions = mapping.get((a, b))
    if questions is None:
        raise ValueError(f"No tie-breaker questions for pair {pair}")
    return questions
