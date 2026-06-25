"""Type-specific wing questions (under-18 scenarios)."""

from __future__ import annotations

from sie.enneagram.questions import Question, _opts
from sie.enneagram.types import wing_types

# 8 questions per primary type — scores go to adjacent wing type numbers directly.


def _wing_q(
    primary: int,
    num: int,
    text: str,
    category: str,
    low_text: str,
    high_text: str,
    low_weight: float = 2.0,
    high_weight: float = 2.0,
) -> Question:
    wing_low, wing_high = wing_types(primary)
    return Question(
        id=f"w{primary}_{num:02d}",
        text=text,
        category=category,
        options=_opts(
            (low_text, {str(wing_low): low_weight}),
            (high_text, {str(wing_high): high_weight}),
        ),
    )


WING_QUESTIONS_TYPE_1: tuple[Question, ...] = (
    _wing_q(1, 1, "クラスのルールが破られたのを見ました。あなたは？", "reaction",
            "静かに見守り、後で先生に報告する", "すぐ声をかけて助ける"),
    _wing_q(1, 2, "テストでミスが出たとき、最初の反応は？", "stress",
            "「次はどうしよう」と一人で計画を立てる", "友達に一緒に復習しようと提案する"),
    _wing_q(1, 3, "休日の過ごし方に近いのは？", "social",
            "一人で好きなことに集中する", "家族や友達の世話をする"),
    _wing_q(1, 4, "意見が対立したとき、あなたは？", "conflict",
            "自分の正しさを保ちつつ距離を取る", "相手の気持ちを優先して譲る"),
    _wing_q(1, 5, "褒められてうれしい言葉は？", "motivation",
            "「落ち着いていて頼もしい」", "「優しくて助けてくれてありがとう」"),
    _wing_q(1, 6, "新しい部活に入った最初の1週間、あなたは？", "expression",
            "様子を見て自分のペースを守る", "先輩や仲間の忙しさを手伝う"),
    _wing_q(1, 7, "親に「もっとゆるくしていい」と言われたら？", "decision",
            "「でも正しい方がいい」と思う", "「人の役に立てればいい」と思う"),
    _wing_q(1, 8, "友達が落ち込んでいます。あなたは？", "relationship",
            "そっとそばにいて、必要なら声をかける", "何か食べ物や手助けを持っていく"),
)

WING_QUESTIONS_TYPE_2: tuple[Question, ...] = (
    _wing_q(2, 1, "友達の秘密を聞きました。あなたは？", "reaction",
            "守るべきルールを優先して慎重に扱う", "相手の気持ちを最優先する"),
    _wing_q(2, 2, "文化祭の準備で、あなたの役割は？", "social",
            "計画表を作り、段取りを確認する", "みんなが楽に進められるよう支援する"),
    _wing_q(2, 3, "努力しても感謝されなかったとき、あなたは？", "stress",
            "「正しいことをした」と自分に言い聞かせる", "「もっと与えれば」と思う"),
    _wing_q(2, 4, "自分の意見を言うとき、あなたは？", "expression",
            "事実と筋道をはっきり伝える", "相手が傷つかないよう柔らかく伝える"),
    _wing_q(2, 5, "目標を立てるとき、近いのは？", "motivation",
            "正しく、誠実に達成する", "周りの人を喜ばせながら達成する"),
    _wing_q(2, 6, "グループで意見が割れたとき、あなたは？", "conflict",
            "正しい方を支持する", "みんなが傷つかない落としどころを探す"),
    _wing_q(2, 7, "SNSで自分をどう見せたい？", "relationship",
            "真面目で信頼できる人", "いつも助けてくれる温かい人"),
    _wing_q(2, 8, "親友とケンカしたあと、あなたは？", "decision",
            "一度整理してから話す", "すぐ仲直りしたいと連絡する"),
)

WING_QUESTIONS_TYPE_3: tuple[Question, ...] = (
    _wing_q(3, 1, "成果が出なかったとき、あなたは？", "stress",
            "落ち込み、自分の気持ちに沈む", "すぐ次の目標に切り替える"),
    _wing_q(3, 2, "クラスで注目されたい理由に近いのは？", "motivation",
            "特別な才能や個性を認めてほしい", "有能で成功していると見られたい"),
    _wing_q(3, 3, "チームで失敗したとき、あなたは？", "reaction",
            "自分の感情を大切にし、意味を考える", "原因を分析して立て直す"),
    _wing_q(3, 4, "友達にどう見られたい？", "relationship",
            "深く、独自の感性がある人", "成果が出ていて頼れる人"),
    _wing_q(3, 5, "忙しい週の過ごし方、近いのは？", "social",
            "一人の時間で気持ちを整える", "予定を詰めて成果を出す"),
    _wing_q(3, 6, "褒め言葉で心に響くのは？", "expression",
            "「あなたらしいね」", "「さすが、結果が出ているね」"),
    _wing_q(3, 7, "進路を選ぶ基準、近いのは？", "decision",
            "自分らしさや意味が大切", "評価や成果が見えること"),
    _wing_q(3, 8, "競争の場面で、あなたは？", "conflict",
            "勝つより、自分の表現を大切にする", "勝ちに行く、結果を出す"),
)

WING_QUESTIONS_TYPE_4: tuple[Question, ...] = (
    _wing_q(4, 1, "感情が強くなったとき、あなたは？", "reaction",
            "一人で深く味わい、表現に移す", "切り替えて次の楽しいことを探す"),
    _wing_q(4, 2, "新しい趣味を始めるとき、あなたは？", "decision",
            "深く調べ、独自のやり方を見つける", "まず試して、広げていく"),
    _wing_q(4, 3, "友達グループで、あなたの役割に近いのは？", "social",
            "雰囲気を作る、盛り上げ役", "深い話ができる特別な存在"),
    _wing_q(4, 4, "傷ついたときの回復方法、近いのは？", "stress",
            "創作や音楽で感情を吐き出す", "友達と遊んで気分転換する"),
    _wing_q(4, 5, "「普通」だと言われたら？", "conflict",
            "少し嬉しい（地に足がつく）", "すごく傷つく"),
    _wing_q(4, 6, "学校行事の準備、あなたは？", "motivation",
            "効率よく、成果を出す方に回る", "世界観や意味を大切にする"),
    _wing_q(4, 7, "親友に話す内容、近いのは？", "relationship",
            "今日楽しかったこと、次の予定", "今感じていること、本音"),
    _wing_q(4, 8, "落ち込んでいる友達に対して、あなたは？", "expression",
            "励まして前向きな話題を出す", "一緒にその感情に寄り添う"),
)

WING_QUESTIONS_TYPE_5: tuple[Question, ...] = (
    _wing_q(5, 1, "知らない番号から着信が。あなたは？", "reaction",
            "慎重に調べてから対応する", "不安だが出てみる"),
    _wing_q(5, 2, "グループワークで、あなたは？", "social",
            "情報を集め、分析する役", "みんなの不安を和らげ、確認する"),
    _wing_q(5, 3, "予定がキャンセルになった。あなたは？", "stress",
            "別の楽しいことを探す", "一人で調べ物や読書を続ける"),
    _wing_q(5, 4, "新しいゲームやアプリ、あなたは？", "decision",
            "仕組みを理解してから使う", "まず触って楽しむ"),
    _wing_q(5, 5, "友達との約束、近いスタイルは？", "relationship",
            "楽しい時間を優先する", "深い話ができる少数の友達"),
    _wing_q(5, 6, "テスト前の過ごし方、近いのは？", "motivation",
            "過去問を解き、不安を減らす", "参考書で理解を深める"),
    _wing_q(5, 7, "クラスで発言するとき、あなたは？", "expression",
            "論理的に、簡潔に", "みんなが安心するよう確認しながら"),
    _wing_q(5, 8, "文化祭の企画、あなたの提案は？", "conflict",
            "安全で確実な、みんなが参加しやすい案", "新しくて知的な案"),
)

WING_QUESTIONS_TYPE_6: tuple[Question, ...] = (
    _wing_q(6, 1, "初対面の場、最初の30分、あなたは？", "social",
            "隅で観察し、情報を集める", "誰かと話して場に馴染む"),
    _wing_q(6, 2, "理不尽な注意を受けた。あなたは？", "conflict",
            "我慢して距離を取る", "すぐ言い返す・主張する"),
    _wing_q(6, 3, "将来が不安な夜、あなたは？", "stress",
            "一人で深く考え、理解しようとする", "信頼できる人に相談する"),
    _wing_q(6, 4, "新しいルールができた。あなたは？", "reaction",
            "なぜそうなったか分析する", "みんなが守れるか心配する"),
    _wing_q(6, 5, "友達を選ぶ基準、近いのは？", "relationship",
            "一緒にいて楽しい、自由な人", "約束を守る、信頼できる人"),
    _wing_q(6, 6, "部活の練習、あなたは？", "motivation",
            "正しいフォーム・ルールを守る", "楽しさや刺激を見つける"),
    _wing_q(6, 7, "意見を言うとき、あなたは？", "expression",
            "はっきり、短く", "根拠を示して慎重に"),
    _wing_q(6, 8, "休日、あなたに近いのは？", "decision",
            "のんびり、好きな人と穏やかに", "新しい場所や友達を探す"),
)

WING_QUESTIONS_TYPE_7: tuple[Question, ...] = (
    _wing_q(7, 1, "友達とケンカした。あなたは？", "conflict",
            "すぐ別の楽しい話題に逃げる", "相手の不安を確認して話し合う"),
    _wing_q(7, 2, "予定が詰まりすぎた週、あなたは？", "stress",
            "一つずつ確認して安心する", "とにかく楽しいことを挟む"),
    _wing_q(7, 3, "新しいクラス、あなたは？", "social",
            "信頼できる人を見つけて固める", "いろんな人とすぐ仲良くなる"),
    _wing_q(7, 4, "理不尽なことを言われた。あなたは？", "reaction",
            "はっきり言い返す", "冗談で流す・話題を変える"),
    _wing_q(7, 5, "目標を達成したあと、あなたは？", "motivation",
            "次の楽しい目標を探す", "チームの安全や信頼を確認する"),
    _wing_q(7, 6, "一人の時間、あなたは？", "relationship",
            "読書や調べ物で深く没頭", "SNSや友達の予定で埋める"),
    _wing_q(7, 7, "文化祭の出し物、あなたの希望は？", "decision",
            "みんなで安心して取り組める企画", "新しくてワクワクする企画"),
    _wing_q(7, 8, "落ち込んでいるとき、あなたは？", "expression",
            "誰かに支えてもらいたい", "一人で楽しいことを探して切り替える"),
)

WING_QUESTIONS_TYPE_8: tuple[Question, ...] = (
    _wing_q(8, 1, "理不尽なことを言われた。あなたは？", "conflict",
            "一度飲み込み、後から距離を取る", "その場ですぐ言い返す"),
    _wing_q(8, 2, "友達との予定がキャンセルに。あなたは？", "stress",
            "別の楽しい予定をすぐ探す", "家でゴロゴロ、特に困らない"),
    _wing_q(8, 3, "グループで意見が割れた。あなたは？", "reaction",
            "みんなが落ち着く方を優先する", "自分の意見をはっきり出す"),
    _wing_q(8, 4, "イライラの出方、近いのは？", "expression",
            "長く溜めて、突然または黙る", "早く、短く、外に向かう"),
    _wing_q(8, 5, "文化祭の役割分担、あなたは？", "social",
            "目立つ役・前に出る役", "裏方・みんなを調整する役"),
    _wing_q(8, 6, "親友とケンカしたあと、あなたは？", "relationship",
            "時間を置いて自然に戻す", "すぐ「嫌いじゃない」と伝える"),
    _wing_q(8, 7, "弱さを見せるとき、あなたは？", "motivation",
            "信頼できる一人にだけ見せる", "あまり見せない、強く見られたい"),
    _wing_q(8, 8, "休日の過ごし方、近いのは？", "decision",
            "のんびり、穏やかに過ごす", "体を動かす・やりたいことを思い切りやる"),
)

WING_QUESTIONS_TYPE_9: tuple[Question, ...] = (
    _wing_q(9, 1, "いじめを見かけた。あなたは？", "conflict",
            "「許せない」と割って入る", "見て見ぬふり、後で本人に声をかける"),
    _wing_q(9, 2, "意見を言うべき場面、あなたは？", "expression",
            "はっきり、短く言う", "言わない、空気を読む"),
    _wing_q(9, 3, "イライラが溜まったとき、あなたは？", "stress",
            "我慢の限界で一気に言い返す", "距離を取って静かに過ごす"),
    _wing_q(9, 4, "リーダー役を任された。あなたは？", "social",
            "前に出て、みんなを動かす", "調整役に徹し、合意を優先する"),
    _wing_q(9, 5, "友達から頼みごとをされた。あなたは？", "reaction",
            "「正しいか」を確認してから動く", "断れず、とりあえず引き受ける"),
    _wing_q(9, 6, "褒められてうれしい言葉は？", "motivation",
            "「頼りになる」「強いね」", "「一緒にいて落ち着く」"),
    _wing_q(9, 7, "進路や部活の選択、あなたは？", "decision",
            "正しさや改善できるかを重視", "穏やかに続けられるかを重視"),
    _wing_q(9, 8, "親友と意見が対立した。あなたは？", "relationship",
            "自分の意見を通す", "相手に合わせて平和を保つ"),
)

WING_QUESTIONS_BY_TYPE: dict[int, tuple[Question, ...]] = {
    1: WING_QUESTIONS_TYPE_1,
    2: WING_QUESTIONS_TYPE_2,
    3: WING_QUESTIONS_TYPE_3,
    4: WING_QUESTIONS_TYPE_4,
    5: WING_QUESTIONS_TYPE_5,
    6: WING_QUESTIONS_TYPE_6,
    7: WING_QUESTIONS_TYPE_7,
    8: WING_QUESTIONS_TYPE_8,
    9: WING_QUESTIONS_TYPE_9,
}


def get_wing_questions(primary_type: int) -> tuple[Question, ...]:
    """Return wing questions for the given primary type (1–9)."""
    if primary_type not in WING_QUESTIONS_BY_TYPE:
        raise ValueError(f"Invalid primary type: {primary_type}")
    return WING_QUESTIONS_BY_TYPE[primary_type]
