"""Question definitions for the four-step Enneagram assessment."""

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
# Step 1: Center determination (12 questions)
# Categories: reaction, attention, emotion, action_priority
# ---------------------------------------------------------------------------

CENTER_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="c01",
        text="予想外の出来事が起きたとき、最初に現れる反応は？",
        category="reaction",
        options=_opts(
            ("体が先に反応し、すぐ動く・止まる", {"body": 2.0}),
            ("誰かの反応や関係への影響を気にする", {"heart": 2.0}),
            ("状況を整理し、意味やリスクを考える", {"head": 2.0}),
        ),
    ),
    Question(
        id="c02",
        text="強い感情（怒り・悲しみ・不安）が湧いたとき、どう扱いますか？",
        category="emotion",
        options=_opts(
            ("抑え込むか、体で発散する", {"body": 2.0}),
            ("誰かに話す・共感を求める", {"heart": 2.0}),
            ("分析して距離を取る", {"head": 2.0}),
        ),
    ),
    Question(
        id="c03",
        text="日常で最も注意が向きやすいのは？",
        category="attention",
        options=_opts(
            ("正しさ・秩序・改善点", {"body": 1.5, "1": 0.5}),
            ("人の気持ち・評価・つながり", {"heart": 2.0}),
            ("情報・可能性・将来のリスク", {"head": 2.0}),
        ),
    ),
    Question(
        id="c04",
        text="ストレス時、行動の優先順位は？",
        category="action_priority",
        options=_opts(
            ("問題を即座に片付け、コントロールを取り戻す", {"body": 2.0}),
            ("関係を保ち、周囲の反応を確認する", {"heart": 2.0}),
            ("情報を集め、選択肢を広げる", {"head": 2.0}),
        ),
    ),
    Question(
        id="c05",
        text="会議や議論で、自然と取る役割に近いのは？",
        category="reaction",
        options=_opts(
            ("方針を決め、場を動かす", {"body": 2.0}),
            ("場の空気を和らげ、調整する", {"heart": 1.0, "body": 1.0}),
            ("論点を整理し、懸念を指摘する", {"head": 2.0}),
        ),
    ),
    Question(
        id="c06",
        text="自分を傷つけやすい言葉に近いのは？",
        category="emotion",
        options=_opts(
            ("「あなたは間違っている」「無責任だ」", {"body": 2.0}),
            ("「あなたは必要ない」「愛されていない」", {"heart": 2.0}),
            ("「あなたは無能だ」「頼れない」", {"head": 2.0}),
        ),
    ),
    Question(
        id="c07",
        text="新しい環境では、まず何に意識が向きますか？",
        category="attention",
        options=_opts(
            ("ルール・役割分担・誰が決定権を持つか", {"body": 2.0}),
            ("誰とどう関わるか、どう見られるか", {"heart": 2.0}),
            ("何を知る必要があるか、何が起きうるか", {"head": 2.0}),
        ),
    ),
    Question(
        id="c08",
        text="衝突が起きたあと、回復の仕方に近いのは？",
        category="reaction",
        options=_opts(
            ("距離を取り、体を動かして発散する", {"body": 2.0}),
            ("話し合い、関係が戻ったか確認する", {"heart": 2.0}),
            ("一人で考え、整理してから動く", {"head": 2.0}),
        ),
    ),
    Question(
        id="c09",
        text="「自分らしさ」を感じる瞬間に近いのは？",
        category="emotion",
        options=_opts(
            ("正しく判断し、問題を解決したとき", {"body": 2.0}),
            ("誰かの役に立ち、認められたとき", {"heart": 2.0}),
            ("深く理解し、洞察を得たとき", {"head": 2.0}),
        ),
    ),
    Question(
        id="c10",
        text="時間があるとき、無意識に選びがちな行動は？",
        category="action_priority",
        options=_opts(
            ("整える・直す・片付ける", {"body": 2.0}),
            ("人に連絡する・SNS・近しい人と過ごす", {"heart": 2.0}),
            ("読む・調べる・計画を立てる", {"head": 2.0}),
        ),
    ),
    Question(
        id="c11",
        text="他人の失敗を見たとき、最初の内心に近いのは？",
        category="reaction",
        options=_opts(
            ("「もっとちゃんとすべきだった」", {"body": 2.0}),
            ("「大丈夫か、どう支えよう」", {"heart": 2.0}),
            ("「なぜそうなったか分析したい」", {"head": 2.0}),
        ),
    ),
    Question(
        id="c12",
        text="長期的な目標を考えるとき、軸になりやすいのは？",
        category="action_priority",
        options=_opts(
            ("正しさ・責任・自分の領域を守ること", {"body": 2.0}),
            ("愛・承認・意味のある関係", {"heart": 2.0}),
            ("安全・自由・可能性の確保", {"head": 2.0}),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Step 2: Type within center (7 questions per center)
# Categories: motivation, fear, desire, behavior_pattern
# ---------------------------------------------------------------------------

BODY_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="tb01",
        text="最も避けたい状況に近いのは？",
        category="fear",
        options=_opts(
            ("弱さを見せて支配されること", {"8": 2.0}),
            ("対立と関係の断絶", {"9": 2.0}),
            ("不完全で間違っていると見られること", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb02",
        text="深い欲求に最も近いのは？",
        category="desire",
        options=_opts(
            ("自分の人生をコントロールすること", {"8": 2.0}),
            ("内外の平和と調和", {"9": 2.0}),
            ("正しく、善であること", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb03",
        text="怒りの出方に近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("我慢の末、一気に爆発する", {"8": 1.5, "1": 0.5}),
            ("飲み込み、距離を取る", {"9": 2.0}),
            ("正しさへの苛立ちとして内側に溜める", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb04",
        text="チームでの動機づけに近いのは？",
        category="motivation",
        options=_opts(
            ("正義と力で守る・導く", {"8": 2.0}),
            ("みんなが穏やかに過ごせるようにする", {"9": 2.0}),
            ("正しい方法で質を上げる", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb05",
        text="プレッシャー下での行動パターンは？",
        category="behavior_pattern",
        options=_opts(
            ("前に出て、主導権を握る", {"8": 2.0}),
            ("合意形成を優先し、自分の意見を後回しにする", {"9": 2.0}),
            ("基準を上げ、細部まで確認する", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb06",
        text="幼少期の「当たり前」に近い信念は？",
        category="motivation",
        options=_opts(
            ("弱いと傷つけられる", {"8": 2.0}),
            ("自分の意見は大したことではない", {"9": 2.0}),
            ("正しくないと認めてもらえない", {"1": 2.0}),
        ),
    ),
    Question(
        id="tb07",
        text="休日の過ごし方に最も近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("自分のプロジェクトや体力消耗系の活動", {"8": 2.0}),
            ("のんびり、好きな人と穏やかに過ごす", {"9": 2.0}),
            ("計画通りに整える・改善する", {"1": 2.0}),
        ),
    ),
)

HEART_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="th01",
        text="最も避けたい状況に近いのは？",
        category="fear",
        options=_opts(
            ("自分だけ愛されていないこと", {"2": 2.0}),
            ("価値のない存在と見られること", {"3": 2.0}),
            ("自分らしさや意味がないこと", {"4": 2.0}),
        ),
    ),
    Question(
        id="th02",
        text="深い欲求に最も近いのは？",
        category="desire",
        options=_opts(
            ("必要とされ、愛されること", {"2": 2.0}),
            ("成功し、認められること", {"3": 2.0}),
            ("本物の自分を見出すこと", {"4": 2.0}),
        ),
    ),
    Question(
        id="th03",
        text="人間関係での行動パターンに近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("相手のニーズを先に満たす", {"2": 2.0}),
            ("成果と印象を整え、評価を得る", {"3": 2.0}),
            ("深いつながりを求め、独自性を大切にする", {"4": 2.0}),
        ),
    ),
    Question(
        id="th04",
        text="称賛されたとき、最も心に響くのは？",
        category="motivation",
        options=_opts(
            ("「あなたのおかげで助かった」", {"2": 2.0}),
            ("「さすが、成果が出ている」", {"3": 2.0}),
            ("「あなたは本当に特別だ」", {"4": 2.0}),
        ),
    ),
    Question(
        id="th05",
        text="拒絶されたときの反応に近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("もっと与えて関係を取り戻そうとする", {"2": 2.0}),
            ("別の成功で価値を証明しようとする", {"3": 2.0}),
            ("距離を取り、内面に深く沈む", {"4": 2.0}),
        ),
    ),
    Question(
        id="th06",
        text="仕事での原動力に近いのは？",
        category="motivation",
        options=_opts(
            ("誰かの役に立つこと", {"2": 2.0}),
            ("目標達成と評価", {"3": 2.0}),
            ("意味と自己表現", {"4": 2.0}),
        ),
    ),
    Question(
        id="th07",
        text="SNSや対人で無意識に見せたい自分に近いのは？",
        category="behavior_pattern",
        options=_opts(
            ("頼れる、温かい存在", {"2": 2.0}),
            ("有能で成功している存在", {"3": 2.0}),
            ("深く、独自の感性を持つ存在", {"4": 2.0}),
        ),
    ),
)

HEAD_TYPE_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="tk01",
        text="最も避けたい状況に近いのは？",
        category="fear",
        options=_opts(
            ("無能で、頼るものがないこと", {"5": 2.0}),
            ("支えがなく、危険にさらされること", {"6": 2.0}),
            ("閉じ込められ、苦痛に耐えられないこと", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk02",
        text="深い欲求に最も近いのは？",
        category="desire",
        options=_opts(
            ("有能で、世界を理解すること", {"5": 2.0}),
            ("安全で、信頼できる支援があること", {"6": 2.0}),
            ("満たされ、幸せであること", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk03",
        text="不確実な状況での行動パターンは？",
        category="behavior_pattern",
        options=_opts(
            ("情報を集め、距離を取って分析する", {"5": 2.0}),
            ("信頼できる人・ルールを確認する", {"6": 2.0}),
            ("楽しい選択肢を探し、前向きに動く", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk04",
        text="学ぶ動機に最も近いのは？",
        category="motivation",
        options=_opts(
            ("理解と掌握のため", {"5": 2.0}),
            ("備えと安心のため", {"6": 2.0}),
            ("可能性と楽しさのため", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk05",
        text="計画が頓挫したときの反応は？",
        category="behavior_pattern",
        options=_opts(
            ("一人で考え直し、知識を深める", {"5": 2.0}),
            ("最悪のシナリオと対策を洗い出す", {"6": 2.0}),
            ("別の楽しいプランに切り替える", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk06",
        text="信頼関係で重視するのは？",
        category="motivation",
        options=_opts(
            ("プライバシーと知的な刺激", {"5": 2.0}),
            ("一貫性と信頼できる約束", {"6": 2.0}),
            ("自由と前向きな時間", {"7": 2.0}),
        ),
    ),
    Question(
        id="tk07",
        text="将来について考えるときの傾向は？",
        category="behavior_pattern",
        options=_opts(
            ("深く調べ、専門性を高める", {"5": 2.0}),
            ("リスク管理とバックアップを重視", {"6": 2.0}),
            ("選択肢を広げ、楽しみを確保", {"7": 2.0}),
        ),
    ),
)

CENTER_TYPE_QUESTIONS: dict[Center, tuple[Question, ...]] = {
    Center.BODY: BODY_TYPE_QUESTIONS,
    Center.HEART: HEART_TYPE_QUESTIONS,
    Center.HEAD: HEAD_TYPE_QUESTIONS,
}

# ---------------------------------------------------------------------------
# Step 3: Wing determination (5 questions)
# Categories: extraversion, action_direction, expression_texture
# ---------------------------------------------------------------------------

WING_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="w01",
        text="社交的な場での自分に近いのは？",
        category="extraversion",
        options=_opts(
            ("控えめで、観察から入る", {"wing_low": 1.0}),
            ("積極的で、場を動かしやすい", {"wing_high": 1.0}),
        ),
    ),
    Question(
        id="w02",
        text="新しい挑戦への向き合い方は？",
        category="action_direction",
        options=_opts(
            ("慎重に準備してから動く", {"wing_low": 1.0}),
            ("まず動いて、試行錯誤する", {"wing_high": 1.0}),
        ),
    ),
    Question(
        id="w03",
        text="自己表現の質感に近いのは？",
        category="expression_texture",
        options=_opts(
            ("内省的・繊細・個人的", {"wing_low": 1.0}),
            ("外向的・明快・行動的", {"wing_high": 1.0}),
        ),
    ),
    Question(
        id="w04",
        text="人と関わるエネルギーの出方は？",
        category="extraversion",
        options=_opts(
            ("少人数・深い関係を好む", {"wing_low": 1.0}),
            ("広く関わり、影響を与えたい", {"wing_high": 1.0}),
        ),
    ),
    Question(
        id="w05",
        text="問題解決で頼りがちなのは？",
        category="action_direction",
        options=_opts(
            ("分析・内面の洞察", {"wing_low": 1.0}),
            ("実行・対人交渉", {"wing_high": 1.0}),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Step 4: Instinctual variant (10 questions)
# Categories: safety (sp), role (so), intimacy (sx)
# ---------------------------------------------------------------------------

INSTINCT_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="i01",
        text="収入・住居・健康について、常に意識している程度は？",
        category="safety",
        options=_opts(
            ("非常に高い", {"sp": 2.0}),
            ("普通", {"sp": 0.5, "so": 0.5}),
            ("低い", {"so": 1.0, "sx": 0.5}),
        ),
    ),
    Question(
        id="i02",
        text="グループでの自分の位置づけ（役割）を意識する度合いは？",
        category="role",
        options=_opts(
            ("低い", {"sp": 1.0}),
            ("高い", {"so": 2.0}),
            ("普通", {"so": 1.0}),
        ),
    ),
    Question(
        id="i03",
        text="特定の一人との深いつながりを求める度合いは？",
        category="intimacy",
        options=_opts(
            ("低い", {"sp": 0.5, "so": 1.0}),
            ("非常に高い", {"sx": 2.0}),
            ("普通", {"sx": 1.0}),
        ),
    ),
    Question(
        id="i04",
        text="お金や備えについて考える頻度は？",
        category="safety",
        options=_opts(
            ("ほぼ毎日", {"sp": 2.0}),
            ("時々", {"sp": 1.0}),
            ("ほとんどない", {"so": 1.0}),
        ),
    ),
    Question(
        id="i05",
        text="所属コミュニティでの評価・立場を気にする度合いは？",
        category="role",
        options=_opts(
            ("あまり気にしない", {"sp": 1.0}),
            ("とても気にする", {"so": 2.0}),
            ("普通", {"so": 1.0, "sx": 0.5}),
        ),
    ),
    Question(
        id="i06",
        text="親密な関係の質と強度を重視する度合いは？",
        category="intimacy",
        options=_opts(
            ("低い", {"sp": 1.0}),
            ("非常に高い", {"sx": 2.0}),
            ("普通", {"sx": 1.0}),
        ),
    ),
    Question(
        id="i07",
        text="ストレス時、最初に守ろうとするのは？",
        category="safety",
        options=_opts(
            ("生活基盤・身体・安全", {"sp": 2.0}),
            ("所属・評価・居場所", {"so": 2.0}),
            ("大切な一人との関係", {"sx": 2.0}),
        ),
    ),
    Question(
        id="i08",
        text="会議や集まりで自然と取る役割に近いのは？",
        category="role",
        options=_opts(
            ("実務・環境づくり", {"sp": 1.5}),
            ("調整・ネットワーク", {"so": 2.0}),
            ("一対一の深い対話", {"sx": 1.5}),
        ),
    ),
    Question(
        id="i09",
        text="理想の週末に最も近いのは？",
        category="intimacy",
        options=_opts(
            ("家でゆっくり、生活を整える", {"sp": 2.0}),
            ("友人・仲間と過ごす", {"so": 2.0}),
            ("特別な一人と深く過ごす", {"sx": 2.0}),
        ),
    ),
    Question(
        id="i10",
        text="人生の優先順位で最も上に来やすいのは？",
        category="safety",
        options=_opts(
            ("安定と備え", {"sp": 2.0}),
            ("つながりと所属", {"so": 2.0}),
            ("情熱と親密さ", {"sx": 2.0}),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Supplementary: behavior log options (multiple choice indices)
# ---------------------------------------------------------------------------

WORK_ROLE_OPTIONS: tuple[str, ...] = (
    "リーダー・決断者",
    "支援・調整役",
    "専門家・分析役",
    "実行・成果重視",
    "平和維持・合意形成",
)

RELATIONSHIP_OPTIONS: tuple[str, ...] = (
    "少数の深い関係を大切にする",
    "広いネットワークを維持する",
    "必要最小限、距離を保つ",
    "役割・評価を意識しやすい",
    "対立を避け、調和を優先する",
)

STRESS_REACTION_OPTIONS: tuple[str, ...] = (
    "怒り・硬直・コントロール",
    "過剰な与え・承認欲求",
    "過剰な活動・成果追求",
    "引きこもり・感情の深掘り",
    "情報収集・距離を取る",
    "不安・確認・最悪想定",
    "逃避・別の楽しみを探す",
    "対立・主導権を握る",
    "無気力・優先順位の放棄",
)


def get_type_questions(center: Center) -> tuple[Question, ...]:
    return CENTER_TYPE_QUESTIONS[center]


def get_all_questions() -> dict[str, tuple[Question, ...]]:
    return {
        "center": CENTER_QUESTIONS,
        "type_body": BODY_TYPE_QUESTIONS,
        "type_heart": HEART_TYPE_QUESTIONS,
        "type_head": HEAD_TYPE_QUESTIONS,
        "wing": WING_QUESTIONS,
        "instinct": INSTINCT_QUESTIONS,
    }
