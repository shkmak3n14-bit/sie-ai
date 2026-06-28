"""Core-emotion center discrimination questions (under-18 scenarios).

These supplement the 15 situational center questions by targeting the
gut / heart / head distinction directly. Each option scores 2.5 (vs 2.0
on base questions) for stronger weight in center totals.
"""

from __future__ import annotations

from sie.enneagram.questions import Question, _opts

# category: core_emotion — weighted higher via option scores

CENTER_CORE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="ce01",
        text="クラス全員の前で、先生に「もっとちゃんとしなさい」と言われました。"
        "その瞬間、いちばん強いのはどれ？",
        category="core_emotion",
        options=_opts(
            ("怒りや反発——「そんな言い方ない」と感じる", {"body": 2.5}),
            ("恥ずかしさ——「みんなの前で…」と顔が熱くなる", {"heart": 2.5}),
            ("頭が動く——「なぜそう言われたか」をすぐ考え始める", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce02",
        text="夜、一人で寝付けないとき。頭の中でいちばん長く続くのは？",
        category="core_emotion",
        options=_opts(
            ("体が張る・足を動かしたい・イライラして眠れない", {"body": 2.5}),
            ("「あの人は今、自分のことをどう思っているか」", {"heart": 2.5}),
            ("「もし明日ああなったら…」と最悪の展開を何度も想像する", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce03",
        text="友達と「一緒に行こう」と約束したのに、当日ドタキャンされました。"
        "最初の反応に近いのは？",
        category="core_emotion",
        options=_opts(
            ("「約束を破った」と腹が立つ。すぐ理由を聞きたくなる", {"body": 2.5}),
            ("「自分は大切じゃないのか」と寂しく、傷つく", {"heart": 2.5}),
            ("「本当に都合が悪いのか、他に理由があるのか」と考える", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce04",
        text="大事なテストの前日、ストレスがピークのとき。"
        "いちばん支配的な感覚は？",
        category="core_emotion",
        options=_opts(
            ("体が硬い・集中できない・イライラする", {"body": 2.5}),
            ("親や先生に落ち込んだ点数を見せたらどう思われるか", {"heart": 2.5}),
            ("出題範囲・時間配分・「落としたらどうなるか」を何度も考える", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce05",
        text="親友にLINEを送ったのに、1日返事がありません。"
        "最初に感じるのは？",
        category="core_emotion",
        options=_opts(
            ("無視された腹立ち——「返事くらいして」と感じる", {"body": 2.5}),
            ("「怒ってる？嫌われた？」と不安で胸がざわつく", {"heart": 2.5}),
            ("「忙しいのか、見てないのか、他に理由があるのか」と推理する", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce06",
        text="次のうち、「これだけは我慢できない」と感じやすいのはどれ？",
        category="core_emotion",
        options=_opts(
            ("理不尽・不公平・自分の領域を勝手に侵されること", {"body": 2.5}),
            ("必要とされていない・誰からも見向きもされないこと", {"heart": 2.5}),
            ("先が読めない・情報が足りない・準備できていないこと", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce07",
        text="授業中、大声で名前を呼ばれて、答えを間違えました。"
        "その直後、いちばん近いのは？",
        category="core_emotion",
        options=_opts(
            ("顔が熱い。言い返したい、または黙って固まる", {"body": 2.5}),
            ("「バカにされている」と感じ、周りの目が気になる", {"heart": 2.5}),
            ("「なぜ間違えたか」「次はどう答えるか」を頭で整理する", {"head": 2.5}),
        ),
    ),
    Question(
        id="ce08",
        text="人生で、これだけは避けたいと本能的に感じるのは？",
        category="core_emotion",
        options=_opts(
            ("コントロールを失う・我慢し続けて爆発しそうになること", {"body": 2.5}),
            ("大切な人から必要とされず、一人ぼっちになること", {"heart": 2.5}),
            ("想定外の出来事・不確かな未来に放り出されること", {"head": 2.5}),
        ),
    ),
)
