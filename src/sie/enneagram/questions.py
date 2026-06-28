"""Question definitions for the four-step Enneagram assessment.

All scenarios are written for experiences before age 18 (school, home, peers).
"""

from __future__ import annotations

from dataclasses import dataclass

from sie.enneagram.types import Center


@dataclass(frozen=True)
class ScoredOption:
    text: str
    scores: dict[str, float]


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    category: str
    options: tuple[ScoredOption, ...]


def _opts(*items: tuple[str, dict[str, float]]) -> tuple[ScoredOption, ...]:
    return tuple(ScoredOption(text=text, scores=scores) for text, scores in items)


# ---------------------------------------------------------------------------
# Step 1: Center determination (15 questions) — under 18
# ---------------------------------------------------------------------------

CENTER_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="c01",
        text="登校中、電車が止まって学校に30分遅れそうです。最初にすることに近いのは？",
        category="reaction",
        options=_opts(
            ("イライラする。早く着けないか探す", {"body": 2.0}),
            ("先生や友達に連絡する", {"heart": 2.0}),
            ("遅延情報や別ルートを調べる", {"head": 2.0}),
        ),
    ),
    Question(
        id="c02",
        text="親と「勉強」のことでケンカして、胸がモヤモヤしています。その夜どう過ごしますか？",
        category="emotion",
        options=_opts(
            ("散歩や運動で体を動かす。または黙って寝る", {"body": 2.0}),
            ("友達にLINEする。「ごめん」と親に言う", {"heart": 2.0}),
            ("なぜああなったか、頭の中で何度も整理する", {"head": 2.0}),
        ),
    ),
    Question(
        id="c03",
        text="クラス替えや転校で、新しいクラスの初日。いちばん気になるのは？",
        category="attention",
        options=_opts(
            ("ルール・座席・誰がリーダーか", {"body": 2.0}),
            ("誰と友達になれるか・どう見られるか", {"heart": 2.0}),
            ("時間割・困ったとき誰に聞けばいいか", {"head": 2.0}),
        ),
    ),
    Question(
        id="c04",
        text="明日、レポートの提出期限です。今日の夕方、友達から「今から遊ぼう」と誘われました。",
        category="action_priority",
        options=_opts(
            ("「先にレポートを終わらせる」と決めているので、遊びに行かない", {"body": 2.0}),
            ("友達をがっかりさせたくなくて、迷いながら断る", {"heart": 2.0}),
            ("レポートに何時間かかるか計算し、短時間だけ会うか決める", {"head": 2.0}),
        ),
    ),
    Question(
        id="c05",
        text="授業のグループワークで、意見が割れてギクシャクしました。あなたは？",
        category="reaction",
        options=_opts(
            ("はっきり自分の意見を言う", {"body": 2.0}),
            ("みんなの気持ちが傷つかないよう、言い方や話題を調整する", {"heart": 2.0}),
            ("一旦黙って、どちらが正しいか考える", {"head": 2.0}),
        ),
    ),
    Question(
        id="c06",
        text="親しい友達や家族に、こんな言葉を言われたらいちばん傷つきますか？",
        category="emotion",
        options=_opts(
            ("「あなたは間違ってる」「約束守れないの？」", {"body": 2.0}),
            ("「あなたがいなくても平気」「邪魔」", {"heart": 2.0}),
            ("「考えが浅い」「頼りにならない」", {"head": 2.0}),
        ),
    ),
    Question(
        id="c07",
        text="高校・中学のオープンスクールに参加しました。最初にチェックするのは？",
        category="attention",
        options=_opts(
            ("校則・設備・通学のしやすさ", {"body": 2.0}),
            ("先輩・生徒の雰囲気・先生の印象", {"heart": 2.0}),
            ("進路・部活・カリキュラムの情報", {"head": 2.0}),
        ),
    ),
    Question(
        id="c08",
        text="クラスメイトと小さなトラブルがあり、気まずい状態です。翌日どうしますか？",
        category="reaction",
        options=_opts(
            ("自分から「あの件どうする？」と切り出す", {"body": 2.0}),
            ("相手の顔色を見て、タイミングを待つ", {"heart": 2.0}),
            ("一度距離を置き、落ち着いてから話す", {"head": 2.0}),
        ),
    ),
    Question(
        id="c09",
        text="「今日は最高だった」と思えるのは、どんなとき？",
        category="emotion",
        options=_opts(
            ("宿題や部活の目標をちゃんと終わらせた", {"body": 2.0}),
            ("友達や先生に「ありがとう」と言われた", {"heart": 2.0}),
            ("ずっと気になっていた問題がスッキリわかった", {"head": 2.0}),
        ),
    ),
    Question(
        id="c10",
        text="急に予定が空きました。午後は自由です。なにをしますか？",
        category="action_priority",
        options=_opts(
            ("部屋の片付け・勉強の遅れを取り戻す", {"body": 2.0}),
            ("友達に連絡する・誰かと会う", {"heart": 2.0}),
            ("読みたい本・調べたいことをする", {"head": 2.0}),
        ),
    ),
    Question(
        id="c11",
        text="部活や委員会で、後輩が同じミスを3回目で繰り返しました。内心どう思いますか？",
        category="reaction",
        options=_opts(
            ("「ちゃんと教えたのに…」とイラッとする", {"body": 2.0}),
            ("「大丈夫かな、困ってないかな」と心配する", {"heart": 2.0}),
            ("「なぜ続くのか、やり方の問題かな」と考える", {"head": 2.0}),
        ),
    ),
    Question(
        id="c12",
        text="高校卒業後の自分を想像するとき、いちばん避けたい状態に近いのは？",
        category="action_priority",
        options=_opts(
            ("自分の軸がブレて、境界を守れないこと", {"body": 2.0}),
            ("大切な人から必要とされず、愛されていないと感じること", {"heart": 2.0}),
            ("先が見えず、心配事が整理できないこと", {"head": 2.0}),
        ),
    ),
    Question(
        id="c13",
        text="学校の食堂で、注文したものと違うものが出てきました。どうしますか？",
        category="reaction",
        options=_opts(
            ("すぐ「違います」と言う", {"body": 2.0}),
            ("相手が困らないか見てから、やんわり言う", {"heart": 2.0}),
            ("このまま食べられるか考えてから動く", {"head": 2.0}),
        ),
    ),
    Question(
        id="c14",
        text="SNSで、同級生の受賞や合格報告を見ました。最初の気持ちに近いのは？",
        category="emotion",
        options=_opts(
            ("「悔しい」「なんで自分だけ…」と腹が立つ、または焦る", {"body": 2.0}),
            ("「すごいな、自分と比べてしまう」", {"heart": 2.0}),
            ("「どうやったんだろう、どれくらい努力したんだろう」", {"head": 2.0}),
        ),
    ),
    Question(
        id="c15",
        text="体調がすぐれない日、学校があります。どうしますか？",
        category="action_priority",
        options=_opts(
            ("行ける限り行く。遅刻はしたくない", {"body": 2.0}),
            ("友達や先生に迷惑がかからないか気にして連絡する", {"heart": 2.0}),
            ("症状と予定を天秤にかけ、無理のない判断をする", {"head": 2.0}),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Step 2: Type within center (9 questions per center) — under 18
# ---------------------------------------------------------------------------

BODY_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="tb01",
        text="学校の廊下で、いじめられている人を見ました。あなたは？",
        category="fear",
        options=_opts(
            ("「許せない」と割って入る、先生を呼ぶ", {"8": 2.0}),
            ("見て見ぬふり。後で本人にそっと声をかける", {"9": 2.0}),
            ("「ルール的にどうなの？」と正しさを気にする", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb02",
        text="学生時代、これだけは避けたい場面に近いのは？",
        category="desire",
        options=_opts(
            ("弱いところを見せて、人にいじめられる", {"8": 2.0}),
            ("親しい友達とケンカして、関係が壊れる", {"9": 2.0}),
            ("テストや当番でミスして「ダメな人」と思われる", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb03",
        text="イライラが溜まったとき（家庭・学校）、出方に近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("我慢の限界で、一気に言い返す", {"8": 2.0}),
            ("黙って距離を置く。部屋にこもる", {"9": 2.0}),
            ("「なんでこうなるの」と正しさへの不満として溜める", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb04",
        text="修学旅行や林間学校で、班の行き先がバラバラになりました。あなたは？",
        category="motivation",
        options=_opts(
            ("「こうしよう」と決めて、みんなを動かす", {"8": 2.0}),
            ("「みんなが楽な方で」と調整する", {"9": 2.0}),
            ("予定表を見直し、公平な案を出す", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb05",
        text="提出期限前日、グループ課題で仲間の部分が遅れています。どうしますか？",
        category="behavior_pattern",
        options=_opts(
            ("「自分がやる」と引き受ける、または厳しく促す", {"8": 2.0}),
            ("自分の分を終えつつ、相手のペースを待つ", {"9": 2.0}),
            ("チェックリストを作り、抜けを確認する", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb06",
        text="小さい頃、「当たり前」だと思っていたことに近いのは？",
        category="motivation",
        options=_opts(
            ("弱いところを見せると、いじめられる", {"8": 2.0}),
            ("自分の意見より、みんなの平和の方が大事", {"9": 2.0}),
            ("ちゃんとしなければ、認めてもらえない", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb07",
        text="日曜日、宿題も部活もない日。いちばん近い過ごし方は？",
        category="behavior_pattern",
        options=_opts(
            ("スポーツ・ゲーム・やりたいことを思い切りやる", {"8": 2.0}),
            ("ゴロゴロ。家族とのんびり", {"9": 2.0}),
            ("部屋の片付け・来週の準備を整える", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb08",
        text="学級会で、明らかに不公平な案が通りそうです。あなたは？",
        category="fear",
        options=_opts(
            ("「それはおかしい」とはっきり止める", {"8": 2.0}),
            ("反対はするが、クラスの空気を壊したくない", {"9": 2.0}),
            ("理由を示して、正しい方向に直す", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb09",
        text="先生や親に褒められて、いちばん嬉しい言葉は？",
        category="desire",
        options=_opts(
            ("「頼りになる」「みんなを守ってくれた」", {"8": 2.0}),
            ("「一緒にいて落ち着く」「優しいね」", {"9": 2.0}),
            ("「丁寧だね」「信頼できる」", {"1": 2.0}),
        ),
    ),
)

HEART_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="th01",
        text="親しい友達の誕生日パーティーに、自分だけ招待されていませんでした。どう感じますか？",
        category="fear",
        options=_opts(
            ("「嫌われた？」と、自分が必要ないと感じる", {"2": 2.0}),
            ("「自分は置いてきぼり」と、価値が下がった気がする", {"3": 2.0}),
            ("「自分だけ取り残された」と、深く傷つく", {"4": 2.0}),
        ),
    ),
    Question(
        id="th02",
        text="学生時代、心の底でこうありたいに近いのは？",
        category="desire",
        options=_opts(
            ("誰かの役に立ち、「必要な人」でいる", {"2": 2.0}),
            ("テストや大会で成果を出し、「できる人」と認められる", {"3": 2.0}),
            ("自分らしさを見つけ、「特別な自分」でいる", {"4": 2.0}),
        ),
    ),
    Question(
        id="th03",
        text="クラス替え後、最初の1週間。あなたの動きに近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("困ってる人を見つけて、声をかける", {"2": 2.0}),
            ("積極的に自己紹介し、目立つ場面を作る", {"3": 2.0}),
            ("様子を見つつ、自分だけの居場所を探す", {"4": 2.0}),
        ),
    ),
    Question(
        id="th04",
        text="先生から、こんな言葉をもらったらうれしい？",
        category="motivation",
        options=_opts(
            ("「クラスの支えになってくれて助かる」", {"2": 2.0}),
            ("「成績が上がった。さすが」", {"3": 2.0}),
            ("「あなたにしか出せない発想だ」", {"4": 2.0}),
        ),
    ),
    Question(
        id="th05",
        text="親友と大げんかしたあと、あなたに近い行動は？",
        category="behavior_pattern",
        options=_opts(
            ("「嫌いじゃない」と伝え、仲直りしたい", {"2": 2.0}),
            ("普段通りに振る舞い、関係を早く正常に戻す", {"3": 2.0}),
            ("一人になって、感情を深く味わう", {"4": 2.0}),
        ),
    ),
    Question(
        id="th06",
        text="部活や進路を選ぶとき、いちばん大事なのは？",
        category="motivation",
        options=_opts(
            ("人の役に立てること", {"2": 2.0}),
            ("評価・結果・成果が見えること", {"3": 2.0}),
            ("自分の感性や意味が活きること", {"4": 2.0}),
        ),
    ),
    Question(
        id="th07",
        text="SNSのプロフィール、自分に近いイメージは？",
        category="behavior_pattern",
        options=_opts(
            ("温かく、頼られる人", {"2": 2.0}),
            ("忙しく、成果を出している人", {"3": 2.0}),
            ("感性豊かで、少しミステリアスな人", {"4": 2.0}),
        ),
    ),
    Question(
        id="th08",
        text="友達が落ち込んでいます。あなたの最初の反応は？",
        category="fear",
        options=_opts(
            ("「何か手伝える？」とすぐ駆け寄る", {"2": 2.0}),
            ("「大丈夫、元気出せ」と励ます", {"3": 2.0}),
            ("「つらいよね」と、一緒にその気持ちに寄り添う", {"4": 2.0}),
        ),
    ),
    Question(
        id="th09",
        text="学生時代、これだけは絶対に嫌、に近いのは？",
        category="desire",
        options=_opts(
            ("助けても「ありがとう」と言われない", {"2": 2.0}),
            ("努力してもテストや大会で認められない", {"3": 2.0}),
            ("「普通でしょ」と、自分の特別さを否定される", {"4": 2.0}),
        ),
    ),
)

HEAD_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="tk01",
        text="新しい科目や部活で、説明が少なくて不安です。最初にすることは？",
        category="fear",
        options=_opts(
            ("教科書や資料を集め、一人で理解する", {"5": 2.0}),
            ("先輩や先生に「これで合ってますか？」と確認する", {"6": 2.0}),
            ("とりあえずやってみて、楽しい部分を探す", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk02",
        text="学生時代、これだけは避けたい、に近いのは？",
        category="desire",
        options=_opts(
            ("わからないのに、知ったかぶりをされる", {"5": 2.0}),
            ("一人きりで、頼る人もいない状態", {"6": 2.0}),
            ("退屈で、毎日が同じことの繰り返し", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk03",
        text="修学旅行先で、急に雨で外に出られなくなりました。あなたは？",
        category="behavior_pattern",
        options=_opts(
            ("ホテルで調べ物。翌日の予定を練り直す", {"5": 2.0}),
            ("安全な場所を確認し、クラスメイトと相談する", {"6": 2.0}),
            ("「室内で楽しめること」を探して切り替える", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk04",
        text="新しい部活や趣味を始めるとき、あなたに近いのは？",
        category="motivation",
        options=_opts(
            ("本や動画で深く勉強してから始める", {"5": 2.0}),
            ("道具・場所・仲間を先にそろえる", {"6": 2.0}),
            ("とにかく試して、楽しい方を広げる", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk05",
        text="楽しみにしていた文化祭のライブが中止になりました。反応に近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("「なぜ中止？」と情報を調べ、納得する", {"5": 2.0}),
            ("「次はいつ？」「代わりの予定は？」と確認する", {"6": 2.0}),
            ("「じゃあ別の楽しいことしよう」と切り替える", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk06",
        text="信頼できる友達とは、どんな関係ですか？",
        category="motivation",
        options=_opts(
            ("深い話は少ないが、お互いの時間を尊重できる", {"5": 2.0}),
            ("困ったとき頼れる、約束を守る人", {"6": 2.0}),
            ("一緒にいて楽しい、新しいことを一緒に試せる人", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk07",
        text="お小遣いやバイト代のことを考えると、あなたに近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("記録をつけ、自分なりの使い方を決める", {"5": 2.0}),
            ("貯金を分けて、足りなくならないよう確認する", {"6": 2.0}),
            ("あまり深く考えず、今楽しむ方が大事", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk08",
        text="知らない番号から着信がありました。あなたは？",
        category="fear",
        options=_opts(
            ("出ない。後で検索してから折り返す", {"5": 2.0}),
            ("「誰だろう、大丈夫かな」と不安になり、出る", {"6": 2.0}),
            ("出る。嫌ならすぐ切ればいいと思う", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk09",
        text="「自分はこういう人間だ」と言うなら、近いのは？",
        category="desire",
        options=_opts(
            ("物事の仕組みがわかる人", {"5": 2.0}),
            ("信頼され、頼られる人", {"6": 2.0}),
            ("楽観的で、可能性を広げる人", {"7": 2.0}),
        ),
    ),
)

CENTER_TYPE_QUESTIONS: dict[Center, tuple[Question, ...]] = {
    Center.BODY: BODY_TYPE_QUESTIONS,
    Center.HEART: HEART_TYPE_QUESTIONS,
    Center.HEAD: HEAD_TYPE_QUESTIONS,
}

# ---------------------------------------------------------------------------
# Step 4: Instinctual variant (12 questions) — under 18
# ---------------------------------------------------------------------------
# Step 3 wing questions: see wing_questions.py (8 questions per primary type)

INSTINCT_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="i01",
        text="お小遣いやお年玉をもらった直後、まず気になるのは？",
        category="safety",
        options=_opts(
            ("残り・使い道・来月足りるか", {"sp": 2.0}),
            ("友達と遊ぶ・ランチの予定", {"so": 1.0, "sx": 0.5}),
            ("欲しかったもの・楽しみの予定", {"sx": 1.0, "so": 0.5}),
        ),
    ),
    Question(
        id="i02",
        text="新しい部活や委員会に入りました。いちばん気になるのは？",
        category="role",
        options=_opts(
            ("自分の生活リズム（睡眠・勉強）が崩れないか", {"sp": 1.5}),
            ("自分はどんな立場か、仲間にどう見られているか", {"so": 2.0}),
            ("気の合う一人と、早く仲良くなれるか", {"sx": 1.5}),
        ),
    ),
    Question(
        id="i03",
        text="親友との時間と、クラスの友達との時間。近いのは？",
        category="intimacy",
        options=_opts(
            ("クラスの友達の方が多くても平気", {"sp": 0.5, "so": 1.5}),
            ("親友との時間を最優先する", {"sx": 2.0}),
            ("バランスを取る。どちらも大事", {"so": 1.0, "sx": 1.0}),
        ),
    ),
    Question(
        id="i04",
        text="貯金箱やアプリ、残高を見る頻度に近いのは？",
        category="safety",
        options=_opts(
            ("こまめに見る", {"sp": 2.0}),
            ("たまに確認する", {"sp": 1.0, "so": 0.5}),
            ("あまり見ない", {"so": 1.0}),
        ),
    ),
    Question(
        id="i05",
        text="クラスのランチグループに、自分だけ呼ばれなかった翌日。近い気持ちは？",
        category="role",
        options=_opts(
            ("特に気にしない", {"sp": 1.5}),
            ("「仲間外れ？」と少し気になる", {"so": 2.0}),
            ("「親友と二人で過ごせた」と思う", {"sx": 1.0}),
        ),
    ),
    Question(
        id="i06",
        text="「本当の親友」は、あなたにとって何人くらい？",
        category="intimacy",
        options=_opts(
            ("0〜1人。深い関係は少なくていい", {"sp": 1.0, "so": 0.5}),
            ("2〜3人。少数と深く付き合う", {"sx": 2.0}),
            ("5人以上。広く付き合う", {"so": 2.0}),
        ),
    ),
    Question(
        id="i07",
        text="突然、大事なテストで赤点を取り、進路に影響しそうだと聞きました。最初に考えるのは？",
        category="safety",
        options=_opts(
            ("どう勉強し直すか・今後の点数", {"sp": 2.0}),
            ("クラスや友達の目・評判", {"so": 2.0}),
            ("親や親友への説明・彼らとの関係", {"sx": 2.0}),
        ),
    ),
    Question(
        id="i08",
        text="文化祭や地域の祭りで、クラスが出店するとき、あなたは？",
        category="role",
        options=_opts(
            ("自分のペースで、無理なく手伝う", {"sp": 1.5}),
            ("役割をもらい、クラスの一員として動く", {"so": 2.0}),
            ("親しい友達と一緒に、楽しく参加する", {"sx": 1.0, "so": 1.0}),
        ),
    ),
    Question(
        id="i09",
        text="理想の日曜日に、いちばん近いのは？",
        category="intimacy",
        options=_opts(
            ("家で寝て、部屋の片付け・好きなこと", {"sp": 2.0}),
            ("友達と集まって、みんなで過ごす", {"so": 2.0}),
            ("親友や好きな人と、二人きりで過ごす", {"sx": 2.0}),
        ),
    ),
    Question(
        id="i10",
        text="学生時代、いちばん大事だと言われたら近いのは？",
        category="safety",
        options=_opts(
            ("健康・お金・安心して暮らすこと", {"sp": 2.0}),
            ("仲間・クラス・居場所があること", {"so": 2.0}),
            ("好きな人とのつながり・情熱", {"sx": 2.0}),
        ),
    ),
    Question(
        id="i11",
        text="進学や転校を考えています。決め手に近いのは？",
        category="safety",
        options=_opts(
            ("通学・学費・生活のしやすさ", {"sp": 2.0}),
            ("学校の雰囲気・クラスの様子", {"so": 2.0}),
            ("親友や好きな人との距離", {"sx": 2.0}),
        ),
    ),
    Question(
        id="i12",
        text="テスト前でストレスが溜まった週の終わり、回復方法に近いのは？",
        category="intimacy",
        options=_opts(
            ("好きな食べ物・風呂・早寝で体を休める", {"sp": 2.0}),
            ("友達と話す・カラオケや散歩", {"so": 2.0}),
            ("親友や好きな人と長電話・一緒にいる", {"sx": 2.0}),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Supplementary: behavior log options (school-age)
# ---------------------------------------------------------------------------

WORK_ROLE_OPTIONS: tuple[str, ...] = (
    "グループのリーダー・決める人",
    "困ってる人を助け、間を取り持つ",
    "調べて、考えてから動く",
    "テストや大会で、結果を出す",
    "みんながケンカしないよう、調整する",
)

RELATIONSHIP_OPTIONS: tuple[str, ...] = (
    "親しい数人と、深く付き合う",
    "クラス中広く、色々な人と話す",
    "必要なときだけ。距離を保つ",
    "評価や、クラスでの立場を気にしやすい",
    "ケンカは避けたい。平和が大事",
)

STRESS_REACTION_OPTIONS: tuple[str, ...] = (
    "イライラする・頑固になる・全部自分でやろうとする",
    "人の役に立ちすぎる・認めてほしくなる",
    "忙しく動き回る・成果を出そうとする",
    "一人になりたい・感情に深く沈む",
    "調べ物をする・人と距離を置く",
    "不安になる・何度も確認する",
    "別の楽しいことを探す・考えないようにする",
    "強く出る・主導権を握ろうとする",
    "動けなくなる・「どうでもいい」と感じる",
)


def get_type_questions(center: Center) -> tuple[Question, ...]:
    from sie.enneagram.type_core_questions import get_type_core_questions

    base = CENTER_TYPE_QUESTIONS[center] + get_type_core_questions(center)
    if center == Center.BODY:
        from sie.enneagram.body_anger_questions import get_body_anger_type_questions

        return base + get_body_anger_type_questions()
    return base


def get_center_questions() -> tuple[Question, ...]:
    """Return all Step 1 center questions (base 15 + core-emotion 8)."""
    from sie.enneagram.center_core_questions import CENTER_CORE_QUESTIONS

    return CENTER_QUESTIONS + CENTER_CORE_QUESTIONS


def get_all_questions() -> dict[str, tuple[Question, ...]]:
    return {
        "center": get_center_questions(),
        "type_body": BODY_TYPE_QUESTIONS,
        "type_heart": HEART_TYPE_QUESTIONS,
        "type_head": HEAD_TYPE_QUESTIONS,
        "instinct": INSTINCT_QUESTIONS,
    }
