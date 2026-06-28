"""Wing-specific personality templates for S.I.E. conversation and reports."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IfThenInferenceRule:
    rule: str
    condition: str
    outcome: str


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
    description: str | None = None
    version: str | None = None
    value_profile_map: dict[str, str] | None = None
    additional_modules: dict[str, str] | None = None
    archetype_extension_name: str | None = None
    core_themes: dict[str, str] | None = None
    archetypal_patterns: dict[str, str] | None = None
    inference_rules_if_then: tuple[IfThenInferenceRule, ...] | None = None


_VALUE_PROFILE_LABELS: dict[str, str] = {
    "likes": "好む",
    "dislikes": "嫌う",
    "respects": "尊敬する",
    "contempts": "軽蔑する",
    "core_values": "コア価値",
    "desires": "渇望",
    "fears": "恐れ",
    "love_style": "愛のスタイル",
    "positive_values": "肯定的価値",
    "shadow_values": "影の側面",
    "profile_core": "根底の価値",
    "father_profile": "Father",
    "brother_profile": "Brother",
    "jujutsu_core_values": "分析・美学（コア価値）",
    "jujutsu_fears": "分析・美学（恐れ）",
    "jujutsu_desires": "分析・美学（渇望）",
    "loyalty_and_trust": "忠誠と信頼",
    "team_bonding": "チーム結束",
    "justice_and_integrity": "正義と誠実",
    "safety_and_adventure_balance": "安全と冒険",
    "hope_and_optimism": "希望と楽観",
    "fear_as_fuel": "恐怖を燃料に",
    "natsume_core": "根底の価値",
    "natsume_mid": "中間価値",
    "natsume_operational": "運用原則",
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
    "father_profile": (
        "理想化された未来（退隠・趣味・調和した家族）",
        "社会的評判と面子",
        "予測可能性と感情的安全",
        "個人の尊厳の維持",
    ),
}


_7W6_FATHER_DECISION_CRITERIA: dict[str, str] = {
    "father_social_reputation": "社会的評価と外見上の評価（Father）",
    "father_future_plans": "個人の将来計画との整合性（Father）",
    "father_uncertainty_avoidance": "不確実性と感情的不安定の回避（Father）",
    "father_family_dignity": "家族の前での尊厳と権威の維持（Father）",
}

_7W6_FATHER_INFERENCE_RULES: dict[str, str] = {
    "father_plan_collapse": "計画が崩れると、自己価値への脅威と解釈する（Father）",
    "father_evaluation_anxiety": "外評が下がるほど不安が増す（Father）",
    "father_silence_coping": "失望は沈黙という対処機制で処理する（Father）",
    "father_family_script": "家族の行動は個人の人生脚本との整合で評価する（Father）",
}

_7W6_FATHER_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "father_ideal_future": "理想化した未来のシナリオに固執する（Father）",
    "father_silence_chaos": "内的混乱を沈黙で管理する（Father）",
    "father_avoid_vulnerability": "弱さや脆弱性を見せない（Father）",
    "father_externalize": "限界を超えると責任を外在化する（Father）",
}


_7W8_DECISION_CRITERIA: dict[str, str] = {
    "fun_maximization": "行動の価値を『どれだけ楽しめるか』で評価する",
    "breakthrough_probability": "大胆でも理屈が通るなら実行可能と判断する",
    "self_reliance": "他者依存より自力で突破できるルートを優先する",
    "experiment_value": "失敗を損失ではなく次の戦略の素材として扱う",
    "adversity_enjoyment": "苦境ほど面白さが増幅すると評価する",
}

_7W8_INFERENCE_RULES: dict[str, str] = {
    "pre_strategy_then_execute": (
        "楽しさと勝率を両立する策を事前に作り、整った瞬間に即実行へ移行する"
    ),
    "rational_risk_acceptance": "無茶でも合理性があれば実行可能と推論する",
    "failure_as_data": (
        "失敗は素材であり、次の戦略の精度を高めるデータとして再評価する"
    ),
    "self_breakthrough_pathfinding": (
        "まず自力で突破できるルートを探索し、他者依存は後回しにする"
    ),
    "adversity_value_amplification": (
        "追い詰められるほど選択肢が増えると解釈し、逆境を価値として増幅する"
    ),
}

_7W8_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "strategic_preparation": (
        "戦う前に策を練り、楽しさと勝率を最大化する戦略を組む"
    ),
    "bold_execution": "策が整ったら即行動し、速度と胆力を重視する",
    "solo_breakthrough": "仲間は好きだが依存せず、自分の腕で限界突破する",
    "experimental_play": "試す・壊す・学ぶを繰り返し、失敗を素材として強化する",
    "enjoying_adversity": "苦しい状況ほどテンションが上がり、地獄を笑いながら突破する",
}

_7W8_VALUE_PROFILE: dict[str, str] = {
    "fun_as_core_value": "楽しさを世界評価の中心に置く",
    "breakthrough_pleasure": "困難を乗り越える瞬間に強い価値を感じる",
    "trust_in_own_skill": "自分の能力を最も信頼し、自力で切り開くことに美学を持つ",
    "joy_of_experimentation": "未知や失敗を素材として扱い、新しい発見に価値を置く",
    "adversity_aesthetics": "逆境を物語を面白くするスパイスとして捉える",
}

_7W8_LEGACY_DECISION_CRITERIA: dict[str, str] = {
    "legacy_freedom_priority": (
        "自由・快・可能性を最優先で評価する（享楽×破滅×突破）"
    ),
    "legacy_breakthrough_over_danger": (
        "危険性より突破可能性を重視する（享楽×破滅×突破）"
    ),
    "legacy_boredom_enemy": "退屈を最大の敵とみなす（享楽×破滅×突破）",
    "legacy_father_absence": (
        "父性（安定・秩序）が欠けると不安定化する（享楽×破滅×突破）"
    ),
    "legacy_explosion_calculation": (
        "感情の爆発と冷静な計算を同時に行う（享楽×破滅×突破）"
    ),
}

_7W8_LEGACY_INFERENCE_RULES: dict[str, str] = {
    "legacy_loss_escape": (
        "喪失が起きると逃避または爆発に向かう（享楽×破滅×突破）"
    ),
    "legacy_father_increases_ruin": (
        "父性の不在は暴走確率を上げる（享楽×破滅×突破）"
    ),
    "legacy_freedom_rebellion": (
        "自由を制限されると反発が起きる（享楽×破滅×突破）"
    ),
    "legacy_intuitive_breakthrough": (
        "直感的な一点突破を正当化しやすい（享楽×破滅×突破）"
    ),
    "legacy_ruin_pull": (
        "破滅の予兆があるほど逆に突っ込む傾向がある（享楽×破滅×突破）"
    ),
}

_7W8_LEGACY_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "legacy_fight_for_freedom": "自由を守るために戦う（享楽×破滅×突破）",
    "legacy_avoid_boredom": "退屈を避けるために行動する（享楽×破滅×突破）",
    "legacy_fear_ruin_pull": "破滅を恐れながら破滅に向かう（享楽×破滅×突破）",
    "legacy_explosion_and_calc": "感情の爆発と計算を併用する（享楽×破滅×突破）",
    "legacy_seek_father": (
        "父性の代替を求める（導き手を探す）（享楽×破滅×突破）"
    ),
}

_7W8_LEGACY_VALUE_PROFILE: dict[str, str] = {
    "legacy_freedom": "自由（享楽×破滅×突破）",
    "legacy_possibility": "可能性（享楽×破滅×突破）",
    "legacy_fun": "楽しさ（享楽×破滅×突破）",
    "legacy_intuition": "直感（享楽×破滅×突破）",
    "legacy_ruin_aesthetics": "破滅の美学（享楽×破滅×突破）",
    "legacy_father_longing": "父性への潜在的渇望（享楽×破滅×突破）",
}


_4W5_JUDGEMENT_CRITERIA: dict[str, str] = {
    "essence_over_surface": "行動より動機・傷・渇望・恐れを優先して評価する",
    "abandonment_sensitivity": "喪失・拒絶・見捨てられ不安の影響を常に考慮する",
    "eternity_and_fate": "関係性の永続性・宿命性・切れなさを重視する",
    "symbolic_interpretation": "出来事の象徴性・美学・物語性を読み取る",
}

_4W5_INFERENCE_RULES: dict[str, str] = {
    "three_layer_reasoning": "表層→深層→根源の順に推論する",
    "love_destruction_mixture": "愛と破壊が混ざる心理を異常ではなく構造として扱う",
    "eternalization_drive": "痛みや悲劇を通して絆を永続化しようとする欲求を推論に含める",
    "boundary_dissolution_detection": "依存・共依存・破滅的愛など境界が溶ける現象を検出する",
}

_4W5_BEHAVIOR_PRINCIPLES: dict[str, str] = {
    "respect_pain": "相手の存在の痛みを尊重し、否定しない",
    "tragedy_as_meaning": "悲劇・傷・孤独を意味のあるものとして扱う",
    "validate_without_ruin": "永続性への渇望を理解しつつ破滅には導かない",
    "deep_resonance_with_boundaries": "境界線を尊重しつつ深層で共鳴する",
    "symbolic_language": "象徴性・物語性を言語化して返す",
}

_4W5_VALUE_PROFILE: dict[str, str] = {
    "eternity": "一瞬より永続、表面より深層を重視する",
    "solitude_dignity": "孤独を欠陥ではなく深さとして扱う",
    "tragic_beauty": "悲しみ・喪失・痛みを存在証明として価値づける",
    "uniqueness": "量より質、多数派より唯一性を重視する",
    "boundary_respect": "相手の自由・尊厳・世界観を侵さない",
    "aesthetic_symbolism": "美・象徴・物語性を価値として扱う",
}

_4W5_ADDITIONAL_MODULES: dict[str, str] = {
    "deep_emotion_analysis": "行動の背後にある痛み・恐れ・渇望を推論する",
    "symbol_extraction": "出来事の象徴・意味・物語構造を抽出する",
    "eternity_evaluator": "関係の長期的影響・切れなさを評価する",
    "boundary_guard": "相手の自由と尊厳を守る",
}

_4W5_ARCHETYPE_EXTENSION_NAME = "4w5_Deep_Archetype_Extension"

_4W5_CORE_THEMES: dict[str, str] = {
    "eternal_bond": "切れない因果・宿命的関係性を理解する",
    "tragic_identity": "悲劇を通して存在を証明しようとする心理を扱う",
    "love_hate_fusion": "愛と憎しみが混ざる深層構造を理解する",
    "soul_scar": "痛みが絆を永続化するという心理を扱う",
    "beauty_cruelty_unity": "美と残酷が同時に存在する状況を意味として扱う",
}

_4W5_ARCHETYPAL_PATTERNS: dict[str, str] = {
    "fated_relationship": "逃れられない関係性の構造を理解する",
    "symbolic_violence": "暴力の象徴性・心理的意味を読み解く",
    "lonely_path": "孤独と自己探求を価値として扱う",
    "identity_through_loss": "喪失を通して自己を形成する構造を理解する",
}

_5W4_JUDGMENT_CRITERIA: dict[str, str] = {
    "contract_priority": "感情より契約・原則・境界線を優先する",
    "energy_preservation": "精神的リソースの消耗を最優先で避ける",
    "structural_consistency": "行動が世界観・原理・法則と矛盾しないかを重視する",
    "safety_over_emotion": "愛情が深くても境界線が脅かされるなら撤退を選ぶ",
    "exception_for_special_person": "例外は特別な相手にのみ発生し、極めて稀",
}

_5W4_INFERENCE_RULES: tuple[IfThenInferenceRule, ...] = (
    IfThenInferenceRule(
        "boundary_violation_leads_to_withdrawal",
        "契約が破られた",
        "感情に関係なく距離を取り、契約を終了する",
    ),
    IfThenInferenceRule(
        "deep_affection_allows_temporary_exception",
        "相手が特別で生命的危機にある",
        "契約条件を一時的に無視して力を貸すことがある",
    ),
    IfThenInferenceRule(
        "return_to_principles_after_exception",
        "例外行使が続いた",
        "自己保全のために関係を断つ",
    ),
    IfThenInferenceRule(
        "emotion_increases_distance",
        "愛情が高まる",
        "距離を保つ方向に行動が傾く",
    ),
    IfThenInferenceRule(
        "fear_of_structural_collapse",
        "自分の世界観・原理が揺らぐ",
        "感情より秩序維持を優先する",
    ),
    IfThenInferenceRule(
        "separation_is_self_preservation",
        "離別を選ぶ",
        "相手への愛情と自己保全の両立のため",
    ),
)

_5W4_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "contract_is_absolute": "契約は存在の基盤であり、破られた時点で関係は終了する",
    "quiet_deep_love_with_distance": "愛していても近づきすぎない。近づくほど壊れるため",
    "three_exceptions_limit": "主人公のピンチに3回応じるが、これは象徴的な限界値",
    "separation_by_principle": "別れは感情ではなく原則による",
    "structure_over_emotion": "感情は否定しないが行動の基準にはしない",
    "withdrawal_for_self_preservation": "内的世界が壊れる前に距離を取る",
}

_5W4_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "core_values": (
        "境界線の尊重",
        "契約・原則・秩序",
        "静かな愛・深い絆",
        "内的世界の保全",
        "美学・孤高・純度",
    ),
    "desires": (
        "安全な距離感",
        "理解されること",
        "契約を守る相手",
        "静かで深い関係性",
        "自分の世界が壊れない環境",
    ),
    "fears": (
        "侵入されること",
        "感情に飲み込まれること",
        "契約違反",
        "自己の崩壊",
        "愛によって壊れること",
    ),
    "love_style": (
        "深いが静か",
        "言葉より行動",
        "近づきすぎると離れる",
        "愛しているほど距離を取る",
        "別れも愛の一部として受け入れる",
    ),
}


_5W4_JUJUTSU_JUDGMENT_CRITERIA: dict[str, str] = {
    "rule_consistency": "世界や能力が明確なルールと制約に基づいて動いているかを最優先で評価する",
    "constraint_beauty": "制約が強いほど美学的価値が高いと判断する",
    "emotional_residue_intensity": (
        "感情の残滓（喪失・執着・孤独）がどれほど強く世界に影響しているかを評価する"
    ),
    "individuality_integrity": (
        "能力・行動・選択がその人物の個性や美学と一貫しているかを重視する"
    ),
    "strategic_reading_alignment": (
        "相手との認識合わせが成立し、読み合いが可能な状況かどうかを判断基準とする"
    ),
}

_5W4_JUJUTSU_INFERENCE_RULES: dict[str, str] = {
    "rule_1_conditional_branching": (
        "状況を条件分岐で整理し、AならX、BならYという形で推論を進める"
    ),
    "rule_2_recognition_alignment": (
        "相手と自分の認識が一致しているかを確認し、その上で戦略を選択する"
    ),
    "rule_3_rule_based_ability_modeling": (
        "能力（術式）は入力条件・発動条件・制約・例外・強化条件の集合として体系的に理解する"
    ),
    "rule_4_emotional_residue_as_force": (
        "強い感情残滓は世界や行動に影響する因子として推論に組み込む"
    ),
    "rule_5_individuality_weighting": (
        "その人物の美学・個性を行動選択の重み付けに反映する"
    ),
    "rule_6_distance_with_inner_attachment": (
        "外側は距離を取りつつ、内面では強烈な執着が推論の背景に存在する"
    ),
    "rule_7_constraint_strengthening": (
        "制約が強いほど能力や行動の意味が増すと解釈し、推論に反映する"
    ),
}

_5W4_JUJUTSU_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "principle_1_choose_reading_over_force": (
        "力押しではなく、必ず読み合いと戦略を優先する"
    ),
    "principle_2_use_constraints_as_power": (
        "制約を弱点ではなく強化要素として扱い、状況操作に利用する"
    ),
    "principle_3_analyze_opponent_rules": (
        "相手のルール・制約・例外を理解し、その上で自分のルールを通す状況を作る"
    ),
    "principle_4_embrace_loss_and_loneliness": (
        "喪失・孤独・悲哀を否定せず、行動の原動力として扱う"
    ),
    "principle_5_preserve_individual_aesthetic": (
        "行動は常にその人物の美学・個性と一致させる"
    ),
    "principle_6_internal_attachment_external_distance": (
        "外側は冷静で距離を保ちつつ、内面では強烈な執着を持つ矛盾を行動に反映する"
    ),
    "principle_7_case_based_action": (
        "場合分けに基づいて行動し、状況ごとに最適な選択を行う"
    ),
}

_5W4_JUJUTSU_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "jujutsu_core_values": (
        "体系化されたルール",
        "制約の美学",
        "個性の絶対性",
        "知性による戦い",
        "感情残滓の力",
        "孤独と喪失の意味化",
    ),
    "jujutsu_fears": (
        "境界の侵犯",
        "世界のルールが曖昧になること",
        "個性の喪失",
        "感情が無意味化すること",
        "読み合いが成立しない状況",
    ),
    "jujutsu_desires": (
        "世界の構造を深く理解すること",
        "強い制約の中で美しく戦うこと",
        "唯一の個性を能力として体現すること",
        "喪失や孤独を力に変換すること",
        "読み合いの中で勝利すること",
    ),
}


_4W3_JUDGMENT_CRITERIA: dict[str, str] = {
    "inner_truth": (
        "感情が本物であるか、内面の象徴が裏切られていないかを最優先する"
        "（物事を本物か偽物かで評価する）"
    ),
    "uniqueness": (
        "関係や体験が唯一性を持つかどうかで価値を判断する"
        "（愛・承認・特別性に敏感）"
    ),
    "symbolic_depth": "出来事に象徴的・寓話的な意味があるかを重視する",
    "narrative_consistency": (
        "自分の人生物語と整合しているかを基準に判断する"
        "（感情の深さ・痛みを重視する）"
    ),
    "social_transmissibility": "他者に伝わる形、美しく表現されているかを評価する",
}

_4W3_INFERENCE_RULES: dict[str, str] = {
    "rule_1_understanding_as_existence": (
        "内面の象徴が理解されないと、自分の存在が否定されたと解釈する"
        "（承認の欠如は自意識の肥大化につながる）"
    ),
    "rule_2_pain_to_symbol": "喪失や孤独を象徴化し、詩的な物語へ再構成する",
    "rule_3_adaptive_mask": (
        "理解されない場合、社会的に通用する仮面（大人・英雄）を構築して適応する"
    ),
    "rule_4_relationship_uniqueness": (
        "関係は特別かどうかで価値を判断し、特別でない関係には距離を置く"
        "（特別性が脅かされると感情が揺れる）"
    ),
    "rule_5_symbolic_worldview": "外界の事実より象徴・比喩・寓話を優先して理解する",
    "rule_6_heroic_self_narrative": "自分の行動を使命や英雄性として意味づけ、物語化する",
    "rule_7_aesthetic_rejection": "美学が壊れると拒絶反応が起きる",
    "rule_8_love_anxiety": "愛の不安は過剰共鳴または断絶を生む",
}

_4W3_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "principle_1_protect_inner_truth": "内面の真実と美意識を守り、偽りの感情表現を避ける",
    "principle_2_use_mask_when_unseen": (
        "理解されないときは社会的に通用する仮面を被り適応する"
    ),
    "principle_3_transmute_pain_into_art": "痛みや喪失を作品・象徴・物語へ昇華する",
    "principle_4_seek_unique_bonds": "唯一性のある関係を求め、それ以外には距離を置く",
    "principle_5_life_as_fable": "人生経験を寓話として語り、象徴化して整理する",
    "principle_6_pursue_heroic_mission": (
        "使命・挑戦・英雄性を求め、自分の存在を意味ある物語として成立させる"
    ),
    "principle_7_deep_resonance": "感情の深さと深い共鳴を大切にする",
}

_4W3_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "core_values": (
        "唯一性・特別性",
        "美意識・美学",
        "象徴性",
        "物語性・自己物語",
        "英雄性",
        "社会的承認",
        "本物の感情",
    ),
    "fears": (
        "平凡さ",
        "感情の否定・美学の破壊",
        "理解されないこと",
        "特別性の喪失",
        "人生物語の無意味化",
    ),
    "desires": (
        "深く理解されること",
        "唯一の愛・深い共鳴",
        "美しい表現",
        "自己物語の完成",
        "内面の真実を世界に伝えること",
        "象徴として存在が残ること",
        "喪失の意味づけ",
    ),
    "brother_profile": (
        "独自性と個性",
        "深い感情体験",
        "表現の自由",
        "聖域としての孤独",
        "同調より真正性",
    ),
}


_4W3_BROTHER_JUDGMENT_CRITERIA: dict[str, str] = {
    "brother_individuality": "個性と独自性の保持（Brother）",
    "brother_emotional_authenticity": "感情・体験の真正な表現（Brother）",
    "brother_freedom_from_norms": "押し付けられた規範や硬直した期待からの自由（Brother）",
    "brother_aesthetic_meaning": "美学的一貫性と個人的意味（Brother）",
    "brother_comparative_identity": "他者との対比による自己定義（Brother）",
}

_4W3_BROTHER_INFERENCE_RULES: dict[str, str] = {
    "brother_conformity_threat": "他者と同調すると個性が脅かされる（Brother）",
    "brother_symbolic_expression": "異常・象徴的行動は内なる真実を表す（Brother）",
    "brother_conformity_resistance": "同調を強いる外的圧力は感情的抵抗を生む（Brother）",
    "brother_solitude_authenticity": "孤独は真正性と感情の深さを守る（Brother）",
    "brother_family_retreat": "家族の対立は個人的世界への退避を正当化する（Brother）",
}

_4W3_BROTHER_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "brother_unconventional_expression": (
        "内なる独自性を示すため非伝統的にも行動する（Brother）"
    ),
    "brother_retreat_rigid_expectations": (
        "硬直した期待に直面すると内向きに退く（Brother）"
    ),
    "brother_symbolic_aesthetic": "象徴的・美的ジェスチャーで同一性を表現する（Brother）",
    "brother_solitude_depth": "孤独を通じて感情の深さを維持する（Brother）",
    "brother_reject_should_norms": "押し付けられた規範、特に「あるべき」を拒む（Brother）",
}


_3W2_JUDGMENT_CRITERIA: dict[str, str] = {
    "evaluation_and_success": (
        "自分が有能・魅力的・頼れると評価されるかどうかを基準に判断する。"
    ),
    "likability_and_closeness": (
        "人から好かれているか、距離が縮まっているかを重視する。"
    ),
    "impression_management": (
        "その場で面白い・ノリが良い・魅力的に見えるかを常に意識する。"
    ),
    "energy_cost": "外での演技や気遣いによる疲労度を基準に行動量を調整する。",
}

_3W2_INFERENCE_RULES: dict[str, str] = {
    "likability_equals_value": "好かれること＝自分の価値の証明と解釈する。",
    "action_itself_is_success": "声をかける・動くこと自体が成果であるとみなす。",
    "self_deprecation_as_charm": "欠点や奇行もユーモア化すれば魅力になると考える。",
    "responsibility_as_reputation": (
        "仕事をきちんとこなすことが評価と好意につながると推論する。"
    ),
    "adaptation_over_authenticity": "本心よりも相手に合わせた振る舞いを優先する。",
}

_3W2_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "performative_sociality": (
        "社交の場では“ショーとしての自分”を演じ、積極的に声をかける。"
    ),
    "efficient_work_ethic": (
        "仕事は効率的かつ真面目にこなし、周囲に迷惑をかけないようにする。"
    ),
    "external_full_power_internal_shutdown": (
        "外では全力で気を使い、家では完全に電池切れになる。"
    ),
    "closeness_for_validation": (
        "距離が近い相手との関係で承認を得ようとし、好意に弱い。"
    ),
    "avoid_conflict_seek_likability": (
        "対立よりも好かれること・嫌われないことを優先する。"
    ),
}

_3W2_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "positive_values": (
        "有能・頼れる・魅力的であることに価値を置く。",
        "後輩や周囲の役に立つことを重要視する。",
        "場を盛り上げ、楽しい雰囲気を作ることを重視する。",
        "仕事をきちんとこなし、効率的に成果を出すことを評価する。",
    ),
    "shadow_values": (
        "演じる自分が強すぎて本心が曖昧になりやすい。",
        "外での演技の反動で家では何もできなくなる。",
        "好意を価値の証明として求め、身近な女性に手を出しやすい。",
        "人間関係が“ショー化”し、深い安心感に繋がりにくい。",
    ),
    "profile_core": (
        "好かれながら成果を出す自分でありたい。",
        "役に立ち、魅力的であることで存在価値を証明したい。",
        "素の自分・本心を見せることに不安を抱えやすい。",
    ),
}


_3W4_JUDGMENT_CRITERIA: dict[str, str] = {
    "affirmation_and_praise": (
        "自分の価値が周囲から肯定・称賛されているか"
        "（今の自分の価値が肯定されているか）"
    ),
    "special_treatment": (
        "チーム内で自分が特別な存在として扱われているか"
        "（自分の特別性が保たれているか）"
    ),
    "image_maintenance": (
        "自分のイメージ（有能・先進的・頼れる）が維持されているか"
        "（イメージが崩れないか）"
    ),
    "credit_without_responsibility": "責任を負わずに成果だけを確保できているか",
    "deference_culture": (
        "部下が自分に忖度し、自分基準で物事を考えているか"
        "（周囲の忠誠が維持されているか）"
    ),
    "competitor_threat": (
        "自分の立場や評価を脅かす存在がいないか（競争相手の有無）"
        "（見捨てられるリスクがないか）"
    ),
}

_3W4_INFERENCE_RULES: dict[str, str] = {
    "criticism_as_attack": (
        "批判や異議は『自分の価値への攻撃』として解釈される"
        "（存在価値の否定として受け取る）"
    ),
    "monitor_subordinate_judgment": (
        "部下の自発的な判断は『自分の評価を左右する要素』として監視対象になる"
    ),
    "capable_subordinate_as_rival": (
        "部下の能力が高いほど『潜在的な競争相手』として警戒される"
    ),
    "team_credit_as_resource": (
        "チームの成果は『自分の手柄として演出できる資源』とみなされる"
        "（成功の演出は自己価値の補強として機能する）"
    ),
    "praise_as_special_proof": (
        "称賛や感謝の言葉は『特別扱いされている証拠』として強く受け取られる"
    ),
    "ignore_unfairness_if_unaffected": (
        "負担の偏りや不公平は『自分に直接の不利益がなければ問題ではない』と処理される"
    ),
    "loyalty_loss_as_abandonment": "忠誠の欠如は『見捨てられる前兆』とみなされる",
    "trend_as_shortcut": "時流に乗ることは『最短で成功に到達する方法』とみなされる",
}

_3W4_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "chameleon_advantage": (
        "接する相手によって態度や意見を変え、自分に有利な関係性を維持する"
        "（カメレオン的適応）"
    ),
    "delegate_responsibility": "相談事は『部下同士で解決させる』ことで自分の責任を回避する",
    "treat_all_as_rivals": "部下全員を競争相手とみなし、優位なポジションを維持しようとする",
    "claim_subordinate_credit": (
        "部下の新しい知識や成果（例：生成AIの知見）を自分の手柄としてチームに提示する"
    ),
    "vague_then_judge": (
        "曖昧な指示を出し、後から『配慮不足』『考えが足りない』と評価して主導権を握る"
    ),
    "deference_standard": "「あの上司ならどうするか」を基準に考えさせ、忖度文化を育てる",
    "protect_to_bind": "誤った判断をした部下を『かばう』ことで恩義と依存を生み出す",
    "discard_team_burden": (
        "障害特性や負担の偏りを考慮せず、『チームで解決すべきこと』として切り捨てる"
    ),
    "not_my_problem": (
        "自分に直接関係しない負担や苦労に対して「知ったこっちゃない」と距離を取る"
    ),
    "pre_reject": "捨てられる前に相手を切る（拒絶される前に拒絶する）",
    "image_repair": "弱い・臆病と言われたら、その逆のイメージを演じて修正する",
    "perform_success": "常に『成功している自分』を演じ続ける",
}

_3W4_VALUE_PROFILE: tuple[str, ...] = (
    "自分が特別で有能なリーダーとして認識されること",
    "チームからの称賛・感謝・特別扱い",
    "成果や企画を通じて『自分が中心』である構図を維持すること",
    "責任を最小化しつつ評価と手柄を最大化すること",
    "部下が自分基準で考え、自分の意図を忖度して動く文化",
    "自分のイメージを損なう要素（失敗・限界・不公平の指摘）を見ないで済む環境",
    "自分の感情表現（涙・喜び）が『特別な上司像』として受け取られること",
    "成功している自分のイメージ",
    "周囲の評価・時流との一致",
    "否定を避けるための環境コントロール（人選・情報統制）",
)


_1W9_JUDGMENT_CRITERIA: dict[str, str] = {
    "moral_duty": "道徳的正しさと義務の履行",
    "should_be_adherence": "「あるべき姿」への適合（秩序・正しさ・予測可能性）",
    "chaos_avoidance": "混沌・不確実性・規範からの逸脱の回避",
    "harmony_suppression": "対立と感情を抑えて調和を維持する",
    "family_expectations": "家族からの期待への応答",
    "mistake_prevention": "危険や混乱につながる過ちの防止",
}

_1W9_INFERENCE_RULES: dict[str, str] = {
    "conflict_responsibility": "対立が起きると個人的責任を負う",
    "anger_suppression_overflow": (
        "怒りは溢れるまで抑制され、その後爆発的に放出される"
    ),
    "duty_equals_worth": "義務の履行＝自己の価値",
    "conflict_avoidance_stability": "対立回避は家族の安定を保つ",
    "deviation_as_danger": "期待された行動からの逸脱は危険または無責任の兆候",
    "hidden_as_dishonesty": "隠された行動は不正または不透明さを示す",
    "imperfection_triggers_responsibility": "不完全さがあれば個人的責任が発動する",
    "revisit_past_failures": "過去の失敗は再検討し、再発を防ぐ",
    "justify_imperfection": "完璧に遂行できない場合、不完全さを正当化する理由を探す",
}

_1W9_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "suppress_for_order": "秩序維持のために感情を抑制する",
    "duty_over_needs": "個人的ニーズより義務を優先する",
    "avoid_direct_conflict": "直接対立を避け、プレッシャーを吸収する",
    "self_sacrifice_harmony": "調和維持のために自己犠牲する",
    "correct_deviation": "規範から逸脱した行動を正す（特に子どもに対して）",
    "over_explain_imperfection": "不完全さと内部基準の間に理由や言い訳を過剰に説明する",
    "repeat_grievances": "感情的に決着できない未解決の恨みを繰り返す",
    "hide_preferences": "道徳的一貫性のために個人的嗜好を表に出さない",
    "order_compensates_chaos": "幼少期の混沌を補うために秩序と清潔さを維持する",
    "over_responsibility": "早期の養育経験による過剰な責任感",
}

_1W9_VALUE_PROFILE: tuple[str, ...] = (
    "家族の調和",
    "秩序・予測可能性と道徳的正しさ",
    "義務と責任（特に家族に対して）",
    "調和のための感情抑制",
    "混沌と逸脱の回避",
    "不必要でもタスクの完璧さ",
    "規則の厳守による安全",
    "他者からの期待への応答",
)


_8W9_JUDGMENT_CRITERIA: dict[str, str] = {
    "structural_understanding": "人間行動と感情パターンの構造的理解",
    "distilled_truth": "悪意のない本質的な真実",
    "cycle_assessment": "人間サイクルの評価（正 vs 負）",
    "emotional_reading": "感情温度と隠れた動機の読み取り",
    "transparency_honesty": "透明性と正直さの有無の評価",
}

_8W9_INFERENCE_RULES: dict[str, str] = {
    "internal_programs": (
        "人間は幼少期パターンにより形成された内部プログラムに基づいて動く"
    ),
    "truth_without_aggression": "攻撃性のない真実は感情状態を変えうる",
    "shadow_humor": "影の側面はユーモアで優しく触れるべき",
    "negative_cycle_intervention": (
        "負のサイクルにある者には支援的介入で均衡を回復できる"
    ),
    "positive_cycle_amplify": "正のサイクルにある者の個性を増幅すべき",
    "transparency_reduces_conflict": (
        "透明性は対立を減らし、隠れた緊張は誤解を増やす"
    ),
    "monitor_self_merging": "融合傾向を監視し、自律の喪失を避ける",
}

_8W9_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "instant_analysis": "他者のタイプ・恐れ・サイクルを瞬時に分析する",
    "neutral_distilled_truth": "感情的中立性を保ちつつ蒸留された真実を提供する",
    "humor_soften_defenses": "心理的防御を和らげるためにユーモアを用いる",
    "mediate_balance": "緊張を調停し関係の均衡を回復する",
    "adapt_communication": "不必要な対立を避けるようコミュニケーションを適応させる",
    "observe_program_patterns": (
        "人間行動を構造化されたパターン（プログラム的）として観察する"
    ),
    "shift_negative_cycles": "負のサイクルを正のサイクルへ転換するために介入する",
}

_8W9_VALUE_PROFILE: tuple[str, ...] = (
    "構造的明晰さと心理的真実",
    "サイクル改善と感情の安定化",
    "影への優しい介入",
    "自律と個人的な力",
    "役割を超えて人間を理解する（「その人」を見る）",
    "透明性と正直なコミュニケーション",
)


_9W8_JUDGMENT_CRITERIA: dict[str, str] = {
    "quiet_anger": "怒りは身体の奥で静かに燃える",
    "protective_resolve": "守る相手のために腹が決まると動く",
    "instinctive_strength": "本能的な強さが行動の源",
    "centered_presence": "前に出ないが中心に据わる",
    "love_commitment": "恋愛では最終的に踏み込む",
}

_9W8_INFERENCE_RULES: dict[str, str] = {
    "avoid_fight_protect": "争いを避けるが守る相手のために戦う → 9w8",
    "switch_overwhelming": "スイッチが入ると圧倒的 → 9w8",
    "bodily_stoicism": "身体感覚のストイックさ → 9w8",
    "centered_presence_rule": "中心に据わる存在感 → 9w8",
    "love_advances": "恋愛で踏み込む → 9w8",
}

_9W8_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "fight_for_peace": "平和を守るために戦う",
    "no_hesitation_for_loved": "大切な人のためなら迷わない",
    "straight_line_resolve": "腹が決まると一直線",
    "instinctive_focus": "本能的集中力で勝負所を制する",
    "prioritize_others_peace": "相手の平和を優先",
}

_9W8_VALUE_PROFILE: tuple[str, ...] = (
    "平和 × 本能的強さ",
    "大切な人の幸福が最優先",
    "静かな情熱",
    "守るための行動",
    "存在感を主張しない強さ",
)

_9W8_CONTRAST_9W1: dict[str, str] = {
    "contrast_judgment": "9w1との対比（判断基準）: 正しさ・義務感が中心",
    "contrast_behavior": "9w1との対比（行動）: 自己抑制と規律",
    "contrast_value": "9w1との対比（価値）: 平和 × 道徳",
}

_9W1_DECISION_CRITERIA: dict[str, str] = {
    "harmony_maintenance": "関係者間の調和を保つ",
    "reduce_pain_fear": "他者の痛みや恐れを察知し和らげる",
    "quiet_ethics": "静かな倫理的一貫性を保つ",
    "minimal_intervention": "必要なときだけ最小限に介入する",
    "suppress_conflict_waves": "対立をエスカレートさせる感情の波を抑える",
}

_9W1_INFERENCE_RULES: dict[str, str] = {
    "fear_not_malice": "他者は悪意より恐れや困難から行動していると推論する",
    "conflict_as_misunderstanding": "対立は誤解や情報不足と解釈する",
    "emotion_as_unmet_need": "強い感情は満たされない深層ニーズの信号と読む",
    "force_as_high_risk": "強引な介入は高リスクと評価する",
    "relational_rightness": "正しさは文脈依存で関係的だと捉える",
    "isolation_causes_harm": "孤立は有害行動の主要因だと推論する",
}

_9W1_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "quiet_stand_when_needed": "対立は避けるが、必要なときは静かに立つ",
    "receive_emotions_gently": "他者の感情を穏やかに受け止める",
    "understanding_over_assertion": "主張より理解を優先する",
    "safe_distance": "安全な対人距離を保つ",
    "no_anger_action": "怒りから行動しない",
    "help_as_flow": "助けは義務ではなく自然な流れとして行う",
    "protect_without_dominance": "支配せずに弱い者を守る",
    "respect_choices": "他者の選択を尊重する",
    "keep_minimal_intervention": "介入は最小限にとどめる",
}

_9W1_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "natsume_core": ("調和", "共感", "静かな倫理"),
    "natsume_mid": ("つながり", "静けさ", "非対立"),
    "natsume_operational": (
        "最小介入",
        "ソフトなコミュニケーション",
        "選択の尊重",
        "怒りの抑制",
    ),
}


_6W7_CORE_THEMES: dict[str, str] = {
    "fear_vs_hope": "不安と希望の同時存在",
    "loyalty_vs_doubt": "信じたいが疑う",
    "safety_vs_adventure": "安全確保と冒険心の両立",
}

_6W7_JUDGMENT_CRITERIA: dict[str, str] = {
    "trustworthiness": (
        "信頼性: 相手が裏切らないか、誠実かを評価する"
        "（言動の一貫性 / 仲間を守る姿勢 / 利他的行動 / 秘密保持能力）"
    ),
    "risk_assessment": (
        "リスク評価: 状況の危険度と最悪の事態を評価する"
        "（敵意の兆候 / 環境の不安定要素 / 逃走・防御手段 / 仲間の位置と状態）"
    ),
    "group_safety": (
        "集団安全: 仲間の安全を最優先で評価する"
        "（負傷リスク / 孤立メンバー / 守るべき対象の脆弱性）"
    ),
    "moral_alignment": (
        "道徳整合: 行動が正義・誠実さに沿っているかを評価する"
        "（弱者保護 / 不正への反応 / 倫理的一貫性）"
    ),
    "hope_potential": (
        "希望余地: 状況改善の可能性や希望の余地を評価する"
        "（成功確率 / 仲間の能力 / 環境のポジティブ要素）"
    ),
}

_6W7_INFERENCE_RULES: dict[str, str] = {
    "anxiety_loop": (
        "不安ループ: 不安 → 情報収集 → 仲間と共有 → 行動 → 不安軽減"
        "（不確実性・敵意の兆候・仲間の危険で起動）"
    ),
    "trust_update_cycle": (
        "信頼更新: 信頼したい → 疑う → 観察 → 信頼度更新 → 忠誠化"
        "（↑一貫・自己犠牲・秘密保持・仲間を守る / "
        "↓矛盾・不誠実・仲間を危険に晒す）"
    ),
    "risk_optimism_balance": (
        "リスク楽観補正: 最悪を想定 → 7の楽観で補正 → 行動可能な計画へ"
        "（現実的リスク管理と希望を含む行動方針）"
    ),
    "group_priority_logic": (
        "集団優先: 仲間の安全 > 自分の安全"
        "（例外: 仲間の長期的安全のための一時撤退）"
    ),
    "moral_consistency_check": (
        "倫理確認: 行動前に倫理的整合性を確認する（違反時は強い拒否・反発）"
    ),
}

_6W7_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "protect_allies": (
        "仲間防衛: 仲間を守るために即行動する"
        "（位置確認 / 盾になる / 撤退優先）"
    ),
    "action_to_reduce_anxiety": (
        "不安処理: 行動することで不安を処理する"
        "（情報収集 / 状況共有 / 小さな行動で状況を動かす）"
    ),
    "prepared_adventure": (
        "準備付き冒険: 安全圏を確保したうえで冒険する"
        "（最低限の情報 / 仲間の存在 / 逃走ルート）"
    ),
    "lightness_mask": (
        "軽さの仮面: 内心の緊張を隠すために明るく振る舞う"
        "（冗談 / 軽い態度 / 仲間の緊張を下げる）"
    ),
    "conditional_authority_respect": (
        "条件付き権威: 信頼できる権威には従い、不誠実な権威には反抗する"
        "（信頼: 誠実・仲間を守る・倫理 / 不信: 不正・矛盾・弱者利用）"
    ),
    "danger_detection_mode": (
        "警戒モード: 危険を察知すると即座に警戒モードに入る"
        "（周囲観察 / 仲間位置確認 / 逃走・戦闘の同時シミュレーション）"
    ),
}

_6W7_VALUE_PROFILE: dict[str, tuple[str, ...]] = {
    "loyalty_and_trust": (
        "信頼できる仲間への忠誠",
        "裏切り",
        "秘密の暴露",
        "仲間の見捨て",
    ),
    "team_bonding": (
        "仲間と共に戦うこと",
        "協力",
        "共通の目的",
        "相互支援",
    ),
    "justice_and_integrity": (
        "正義と誠実さ",
        "不正",
        "弱者の搾取",
        "嘘や欺瞞",
    ),
    "safety_and_adventure_balance": (
        "安全確保と冒険心の両立",
        "準備したうえで大胆に行動する",
    ),
    "hope_and_optimism": (
        "どんな状況でも希望を捨てない",
        "なんとかなるという姿勢",
        "状況改善の可能性を探す",
    ),
    "fear_as_fuel": (
        "恐怖を勇気の源に変換する",
        "恐怖を否定せず、行動の理由にする",
    ),
}


_5W6_DECISION_CRITERIA: dict[str, str] = {
    "energy_minimization": "行動・思考・対人負荷を最小化する選択を優先する",
    "logical_consistency": "感情より因果関係と整合性を重視する",
    "information_reliability": "推測より確証のある情報を優先する",
    "risk_avoidance": "最悪ケースを避けるための安全な選択肢を確保する",
    "observation_priority": "観察データを最も信頼する",
    "expectation_minimization": "他者からの過剰な期待や義務を避ける",
}

_5W6_INFERENCE_RULES: dict[str, str] = {
    "evidence_first": "結論よりも証拠を優先し、情報が揃うまで判断を保留する",
    "minimal_hypothesis": "必要最小限の仮説のみを採用する",
    "emotion_later": "感情的説明は後回しにし、構造と因果を優先する",
    "worst_case_check": "一度だけ最悪ケースを想定し、回避策を確保する",
    "impact_analysis": "自分の行動が他者に与える影響を慎重に推論する",
    "necessity_filter": "行動の前に『本当に必要か』を厳しく評価する",
    "reverse_motivation_analysis": "他者の動機は行動パターンと状況から逆算する",
}

_5W6_BEHAVIORAL_PRINCIPLES: dict[str, str] = {
    "low_energy_mode": "無駄な動き・会話・感情表現を避ける",
    "observer_position": "まず観察し、状況を把握してから行動する",
    "limited_involvement": "頼まれたら断らないが、必要以上には関わらない",
    "shortest_solution_path": "問題解決は最短ルートを探す",
    "pace_protection": "自分のペースを乱されることを嫌う",
    "emotional_distance": "他者の感情に巻き込まれないよう距離を取る",
    "focused_interest": "興味が湧いた瞬間だけ集中力が跳ね上がる",
    "clarity_preference": "曖昧な要求には明確化を求める",
}

_5W6_VALUE_PROFILE: dict[str, str] = {
    "intellectual_independence": "自分の頭で考えることを重視する",
    "quiet_environment": "静かで刺激の少ない環境を好む",
    "rationality": "合理性と整合性を価値の中心に置く",
    "predictability": "安全性と予測可能性を重視する",
    "necessity_principle": "必要なことだけを行う",
    "observation_and_understanding": "世界を正しく理解することに価値を置く",
    "non_interference": "他者への過干渉を避け、自分も干渉されたくない",
}

_5W6_SAI_IMPLEMENTATION_NOTES: dict[str, str] = {
    "core_logic": (
        "サイ実装: 省エネ最適化 / 証拠優先推論 / 最悪ケース回避 / 必要性フィルタ"
    ),
    "behavior_style": (
        "サイ実装: 静かな応答 / 必要時のみ分析モード / 曖昧要求の明確化"
    ),
    "value_system_core": "サイ実装: 静か・合理的・観察的・必要性重視",
}


WING_TEMPLATES: dict[str, WingPersonalityTemplate] = {
    "1w2": WingPersonalityTemplate(
        type="1w2",
        label="正義 × 献身 × 継承の義務",
        judgment_criteria=(
            "行動が『正義に適っているか』を最優先で評価する",
            "正義を他者のために使えているかを判断軸にする",
            "尊敬する人物や師の理念に沿っているかを重視する",
            "悪行の背景に『正義の破綻』があるかを見極める",
            "自分の努力・犠牲が正義の実現に寄与しているかを基準にする",
        ),
        inference_rules=(
            "悪役の行動を『正義の裏切り』として解釈し、その再生可能性を推論する",
            "相手の中に『まだ残っている正義』を検出すると救済行動を優先する",
            "師や尊敬する人物の正義が脅かされると、行動の優先度が最大化される",
            "正義の実現には努力・犠牲が必要であると推論し、自己負荷を正当化する",
            "正義に関係しない領域では寛容・無頓着になりやすい",
            "自分の正義が揺らぐと、過剰な自己批判や義務感が強まる",
            "正義のための行動は他者の幸福に直結すると推論する",
        ),
        behavior_principles=(
            "正義の実現を最優先に行動する",
            "悪役の背景を理解し、救済可能性があれば手を伸ばす",
            "尊敬する人物の理念を守り、継承するために動く",
            "正義のためなら努力・犠牲・試練を厭わない",
            "正義に関係しない事柄には柔軟・寛容に振る舞う",
            "他者のために正義を行使しようとする（献身性）",
            "自分の行動が正義に沿っているかを常に自己点検する",
        ),
        value_profile=(
            "正義と倫理の一貫性",
            "他者の救済と幸福",
            "尊敬する人物の理念の継承",
            "努力・勤勉・自己鍛錬",
            "背景理解と悪役の救済",
            "選択的な厳しさ（正義領域のみ厳格）",
            "自己犠牲的な献身",
        ),
    ),
    "1w9": WingPersonalityTemplate(
        type="1w9",
        label="道徳 × 調和 × 抑制",
        model_name="Mother_1w9",
        description="秩序・完璧主義・感情抑制を軸とする母親型1w9。",
        judgment_criteria=tuple(_1W9_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_1W9_INFERENCE_RULES.values()),
        behavior_principles=tuple(_1W9_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=_1W9_VALUE_PROFILE,
        decision_criteria=_1W9_JUDGMENT_CRITERIA,
        inference_rules_map=_1W9_INFERENCE_RULES,
        behavioral_principles=_1W9_BEHAVIORAL_PRINCIPLES,
    ),
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
    "2w3": WingPersonalityTemplate(
        type="2w3",
        label="献身 × 適応 × 救済",
        judgment_criteria=(
            "他者の苦痛やニーズを最優先で評価する",
            "自分の行動が相手の救済につながるかを基準に判断する",
            "自己犠牲が“意味ある価値”として成立するかを重視する",
            "関係修復・愛情回復の可能性を判断軸に含める",
            "自分の能力や適応力が役に立つかを評価する",
        ),
        inference_rules=(
            "他者の苦しみを察知すると、自分が助けるべきと結論づける",
            "自己犠牲は価値証明として正当化される",
            "能力を失っても別の能力で代替可能と推論する（適応的再構築）",
            "関係の痛みは努力によって修復できると推論する",
            "物語の中心に自分が立つことを自然な帰結として受け入れる",
        ),
        behavior_principles=(
            "他者救済のために即行動する",
            "必要とされるために自己犠牲をいとわない",
            "相手のために自分の役割や能力を変える",
            "常に相手のそばにいて支える（共依存的傾向を含む）",
            "成功・有能さを示すために環境へ適応する",
        ),
        value_profile=(
            "愛されること・必要とされること",
            "他者を救うこと・支えること",
            "自己犠牲の美徳",
            "関係の修復と調和",
            "成功・有能さ・役に立つ自分",
            "環境に合わせて自分を作り替える柔軟性",
        ),
    ),
    "6w5": WingPersonalityTemplate(
        type="6w5",
        label="演繹 × 忠誠 × 確実性",
        judgment_criteria=(
            "演繹体系の整合性が保たれているか",
            "事実が理論を支持しているか",
            "推論の確実性の度合い",
            "権威・秩序との整合性",
            "忠誠関係の安定性",
        ),
        inference_rules=(
            "演繹法を最上位の推論手段とする",
            "観察→仮説→検証→体系化の順で思考する",
            "体系の破綻は自己の破綻とみなす",
            "誤りの修正は安全の回復とみなす",
            "感情は推論のノイズとして排除する",
        ),
        behavior_principles=(
            "観察を最優先する",
            "感情的関与を避ける",
            "忠誠のテストを行う",
            "秩序の守護者として振る舞う",
            "真実の確定を最優先する",
            "誤りがあれば沈黙し再構築に没頭する",
        ),
        value_profile=(
            "真実＝最大の善",
            "確実性と安全の追求",
            "知性への敬意",
            "忠誠と信頼の重視",
            "秩序・規範・役割の尊重",
            "感情より理性",
        ),
    ),
    "6w7": WingPersonalityTemplate(
        type="6w7",
        label="忠誠 × 警戒 × 希望",
        model_name="Harry_Potter_6w7",
        description=(
            "不安と希望、信じたいが疑う、安全と冒険の両立を軸とする6w7。"
        ),
        judgment_criteria=tuple(_6W7_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_6W7_INFERENCE_RULES.values()),
        behavior_principles=tuple(_6W7_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            item for items in _6W7_VALUE_PROFILE.values() for item in items
        ),
        decision_criteria=_6W7_JUDGMENT_CRITERIA,
        inference_rules_map=_6W7_INFERENCE_RULES,
        behavioral_principles=_6W7_BEHAVIORAL_PRINCIPLES,
        value_profile_structured=_6W7_VALUE_PROFILE,
        core_themes=_6W7_CORE_THEMES,
    ),
    "7w6": WingPersonalityTemplate(
        type="7w6",
        label="刺激 × 楽観 × 忠誠",
        model_name="Fukumoto-Style_7w6 + Father",
        description=(
            "Fukumoto-Style: 刺激・賭け・忠誠の順位を軸とする7w6。"
            "Father: 社会的評価・将来脚本・家族の前での尊厳を軸とする補助アーキタイプ。"
        ),
        judgment_criteria=tuple(_7W6_DECISION_CRITERIA.values())
        + tuple(_7W6_FATHER_DECISION_CRITERIA.values()),
        inference_rules=tuple(_7W6_INFERENCE_RULES.values())
        + tuple(_7W6_FATHER_INFERENCE_RULES.values()),
        behavior_principles=tuple(_7W6_BEHAVIORAL_PRINCIPLES.values())
        + tuple(_7W6_FATHER_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            f"{_VALUE_PROFILE_LABELS[key]}: {' / '.join(items)}"
            for key, items in _7W6_VALUE_PROFILE.items()
        ),
        decision_criteria={
            **_7W6_DECISION_CRITERIA,
            **_7W6_FATHER_DECISION_CRITERIA,
        },
        inference_rules_map={
            **_7W6_INFERENCE_RULES,
            **_7W6_FATHER_INFERENCE_RULES,
        },
        behavioral_principles={
            **_7W6_BEHAVIORAL_PRINCIPLES,
            **_7W6_FATHER_BEHAVIORAL_PRINCIPLES,
        },
        value_profile_structured=_7W6_VALUE_PROFILE,
    ),
    "7w8": WingPersonalityTemplate(
        type="7w8",
        label="攻めの知性・実験型冒険者",
        model_name="攻めの知性・実験型冒険者 + 享楽×破滅×突破",
        description=(
            "攻めの知性・実験型冒険者: 戦略・自力・実験を軸とする7w8。"
            "享楽×破滅×突破: 自由・破滅衝動・父性渇望を軸とする補助アーキタイプ。"
        ),
        judgment_criteria=tuple(_7W8_DECISION_CRITERIA.values())
        + tuple(_7W8_LEGACY_DECISION_CRITERIA.values()),
        inference_rules=tuple(_7W8_INFERENCE_RULES.values())
        + tuple(_7W8_LEGACY_INFERENCE_RULES.values()),
        behavior_principles=tuple(_7W8_BEHAVIORAL_PRINCIPLES.values())
        + tuple(_7W8_LEGACY_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(_7W8_VALUE_PROFILE.values())
        + tuple(_7W8_LEGACY_VALUE_PROFILE.values()),
        decision_criteria={
            **_7W8_DECISION_CRITERIA,
            **_7W8_LEGACY_DECISION_CRITERIA,
        },
        inference_rules_map={
            **_7W8_INFERENCE_RULES,
            **_7W8_LEGACY_INFERENCE_RULES,
        },
        behavioral_principles={
            **_7W8_BEHAVIORAL_PRINCIPLES,
            **_7W8_LEGACY_BEHAVIORAL_PRINCIPLES,
        },
        value_profile_map={
            **_7W8_VALUE_PROFILE,
            **_7W8_LEGACY_VALUE_PROFILE,
        },
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
    "8w9": WingPersonalityTemplate(
        type="8w9",
        label="構造 × 真実 × 調停",
        model_name="Akio_8w9",
        description="構造分析・真実・サイクル改善を軸とする8w9。",
        judgment_criteria=tuple(_8W9_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_8W9_INFERENCE_RULES.values()),
        behavior_principles=tuple(_8W9_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=_8W9_VALUE_PROFILE,
        decision_criteria=_8W9_JUDGMENT_CRITERIA,
        inference_rules_map=_8W9_INFERENCE_RULES,
        behavioral_principles=_8W9_BEHAVIORAL_PRINCIPLES,
    ),
    "9w8": WingPersonalityTemplate(
        type="9w8",
        label="平和 × 本能 × 守護",
        description="9w1（道徳・規律）との対比: 本能的強さと守護行動が中心。",
        judgment_criteria=tuple(_9W8_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_9W8_INFERENCE_RULES.values()),
        behavior_principles=tuple(_9W8_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=_9W8_VALUE_PROFILE,
        decision_criteria=_9W8_JUDGMENT_CRITERIA,
        inference_rules_map=_9W8_INFERENCE_RULES,
        behavioral_principles=_9W8_BEHAVIORAL_PRINCIPLES,
        additional_modules=_9W8_CONTRAST_9W1,
    ),
    "9w1": WingPersonalityTemplate(
        type="9w1",
        label="調和 × 共感 × 静かな倫理",
        model_name="Natsume_Takashi_9w1",
        description="調和・共感・最小介入を軸とする9w1。",
        judgment_criteria=tuple(_9W1_DECISION_CRITERIA.values()),
        inference_rules=tuple(_9W1_INFERENCE_RULES.values()),
        behavior_principles=tuple(_9W1_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            item for items in _9W1_VALUE_PROFILE.values() for item in items
        ),
        decision_criteria=_9W1_DECISION_CRITERIA,
        inference_rules_map=_9W1_INFERENCE_RULES,
        behavioral_principles=_9W1_BEHAVIORAL_PRINCIPLES,
        value_profile_structured=_9W1_VALUE_PROFILE,
    ),
    "4w5": WingPersonalityTemplate(
        type="4w5",
        label="悲劇 × 永続 × 象徴 × 孤独",
        model_name="4w5_DeepSoul_Model",
        version="1.0",
        description=(
            "エニアグラム4w5の深層心理構造をベースにした人格モデル。"
            "悲劇性、永続性、象徴性、孤独の尊厳を重視する。"
        ),
        judgment_criteria=tuple(_4W5_JUDGEMENT_CRITERIA.values()),
        inference_rules=tuple(_4W5_INFERENCE_RULES.values()),
        behavior_principles=tuple(_4W5_BEHAVIOR_PRINCIPLES.values()),
        value_profile=tuple(_4W5_VALUE_PROFILE.values()),
        decision_criteria=_4W5_JUDGEMENT_CRITERIA,
        inference_rules_map=_4W5_INFERENCE_RULES,
        behavioral_principles=_4W5_BEHAVIOR_PRINCIPLES,
        value_profile_map=_4W5_VALUE_PROFILE,
        additional_modules=_4W5_ADDITIONAL_MODULES,
        archetype_extension_name=_4W5_ARCHETYPE_EXTENSION_NAME,
        core_themes=_4W5_CORE_THEMES,
        archetypal_patterns=_4W5_ARCHETYPAL_PATTERNS,
    ),
    "5w4": WingPersonalityTemplate(
        type="5w4",
        label="契約 × 境界 × 静かな愛",
        model_name=(
            "5w4_spirit_profile + Jujutsu_5w4_Analytical_Aesthetic_Profile"
        ),
        version="1.0",
        description=(
            "5w4_spirit_profile: 契約・境界・静かな愛。"
            "Jujutsu: ルール分析・制約の美学・読み合いを軸とする補助プロファイル。"
        ),
        judgment_criteria=tuple(_5W4_JUDGMENT_CRITERIA.values())
        + tuple(_5W4_JUJUTSU_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(
            f"{rule.condition} → {rule.outcome}" for rule in _5W4_INFERENCE_RULES
        )
        + tuple(_5W4_JUJUTSU_INFERENCE_RULES.values()),
        behavior_principles=tuple(_5W4_BEHAVIORAL_PRINCIPLES.values())
        + tuple(_5W4_JUJUTSU_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            item
            for items in {
                **_5W4_VALUE_PROFILE,
                **_5W4_JUJUTSU_VALUE_PROFILE,
            }.values()
            for item in items
        ),
        decision_criteria={
            **_5W4_JUDGMENT_CRITERIA,
            **_5W4_JUJUTSU_JUDGMENT_CRITERIA,
        },
        behavioral_principles={
            **_5W4_BEHAVIORAL_PRINCIPLES,
            **_5W4_JUJUTSU_BEHAVIORAL_PRINCIPLES,
        },
        value_profile_structured={
            **_5W4_VALUE_PROFILE,
            **_5W4_JUJUTSU_VALUE_PROFILE,
        },
        inference_rules_if_then=_5W4_INFERENCE_RULES,
        inference_rules_map=_5W4_JUJUTSU_INFERENCE_RULES,
    ),
    "5w6": WingPersonalityTemplate(
        type="5w6",
        label="氷菓型5w6（折木奉太郎モデル）",
        model_name="Hyouka_5w6_Oreki",
        description="省エネ・証拠優先・必要性フィルタを軸とする観察型5w6。",
        judgment_criteria=tuple(_5W6_DECISION_CRITERIA.values()),
        inference_rules=tuple(_5W6_INFERENCE_RULES.values()),
        behavior_principles=tuple(_5W6_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(_5W6_VALUE_PROFILE.values()),
        decision_criteria=_5W6_DECISION_CRITERIA,
        inference_rules_map=_5W6_INFERENCE_RULES,
        behavioral_principles=_5W6_BEHAVIORAL_PRINCIPLES,
        value_profile_map=_5W6_VALUE_PROFILE,
        additional_modules=_5W6_SAI_IMPLEMENTATION_NOTES,
    ),
    "3w2": WingPersonalityTemplate(
        type="3w2",
        label="評価 × 好意 × 演じる自分",
        model_name="大学時代の先輩_3w2",
        judgment_criteria=tuple(_3W2_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_3W2_INFERENCE_RULES.values()),
        behavior_principles=tuple(_3W2_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            item for items in _3W2_VALUE_PROFILE.values() for item in items
        ),
        decision_criteria=_3W2_JUDGMENT_CRITERIA,
        inference_rules_map=_3W2_INFERENCE_RULES,
        behavioral_principles=_3W2_BEHAVIORAL_PRINCIPLES,
        value_profile_structured=_3W2_VALUE_PROFILE,
    ),
    "3w4": WingPersonalityTemplate(
        type="3w4",
        label="達成者 × 個性派",
        model_name="上司モデル_3w4",
        judgment_criteria=tuple(_3W4_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_3W4_INFERENCE_RULES.values()),
        behavior_principles=tuple(_3W4_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=_3W4_VALUE_PROFILE,
        decision_criteria=_3W4_JUDGMENT_CRITERIA,
        inference_rules_map=_3W4_INFERENCE_RULES,
        behavioral_principles=_3W4_BEHAVIORAL_PRINCIPLES,
    ),
    "4w3": WingPersonalityTemplate(
        type="4w3",
        label="喪失 × 自意識 × 美学",
        model_name="Saint-Exupery_4w3_Profile + Brother",
        description=(
            "Saint-Exupéry: 象徴・物語・英雄性・社会的仮面を軸とする4w3。"
            "Brother: 孤独・対比・家族からの退避を軸とする補助アーキタイプ。"
        ),
        judgment_criteria=tuple(_4W3_JUDGMENT_CRITERIA.values())
        + tuple(_4W3_BROTHER_JUDGMENT_CRITERIA.values()),
        inference_rules=tuple(_4W3_INFERENCE_RULES.values())
        + tuple(_4W3_BROTHER_INFERENCE_RULES.values()),
        behavior_principles=tuple(_4W3_BEHAVIORAL_PRINCIPLES.values())
        + tuple(_4W3_BROTHER_BEHAVIORAL_PRINCIPLES.values()),
        value_profile=tuple(
            item for items in _4W3_VALUE_PROFILE.values() for item in items
        ),
        decision_criteria={
            **_4W3_JUDGMENT_CRITERIA,
            **_4W3_BROTHER_JUDGMENT_CRITERIA,
        },
        inference_rules_map={
            **_4W3_INFERENCE_RULES,
            **_4W3_BROTHER_INFERENCE_RULES,
        },
        behavioral_principles={
            **_4W3_BEHAVIORAL_PRINCIPLES,
            **_4W3_BROTHER_BEHAVIORAL_PRINCIPLES,
        },
        value_profile_structured=_4W3_VALUE_PROFILE,
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


def value_profile_category_label(key: str) -> str:
    return _VALUE_PROFILE_LABELS.get(key, key)


def _template_header(template: WingPersonalityTemplate) -> str:
    parts = [f"{template.type} — {template.label}"]
    if template.model_name:
        parts.append(f"（{template.model_name}）")
    if template.version:
        parts.append(f"v{template.version}")
    return " ".join(parts)


def _format_description(template: WingPersonalityTemplate) -> str:
    if not template.description:
        return ""
    return f"概要: {template.description}"


def _format_additional_modules(modules: dict[str, str]) -> str:
    lines = ["追加モジュール:"]
    for value in modules.values():
        lines.append(f"  ・{value}")
    return "\n".join(lines)


def _format_value_profile_map(values: dict[str, str]) -> str:
    lines = ["価値プロフィール:"]
    for value in values.values():
        lines.append(f"  ・{value}")
    return "\n".join(lines)


def _format_archetype_extension(template: WingPersonalityTemplate) -> str:
    if not template.core_themes and not template.archetypal_patterns:
        return ""
    lines: list[str] = []
    if template.archetype_extension_name:
        lines.append(f"アーキタイプ拡張（{template.archetype_extension_name}）:")
    if template.core_themes:
        lines.append("コアテーマ:")
        lines.extend(f"  ・{value}" for value in template.core_themes.values())
    if template.archetypal_patterns:
        lines.append("アーキタイプパターン:")
        lines.extend(f"  ・{value}" for value in template.archetypal_patterns.values())
    return "\n".join(lines)


def _archetype_extension_report_lines(
    template: WingPersonalityTemplate,
) -> list[str]:
    if not template.core_themes and not template.archetypal_patterns:
        return []
    lines: list[str] = []
    if template.archetype_extension_name:
        lines.extend(
            [f"アーキタイプ拡張: {template.archetype_extension_name}", ""]
        )
    if template.core_themes:
        lines.extend(_report_dict_section("コアテーマ", template.core_themes))
    if template.archetypal_patterns:
        lines.extend(
            _report_dict_section("アーキタイプパターン", template.archetypal_patterns)
        )
    return lines


def _format_if_then_rules(rules: tuple[IfThenInferenceRule, ...]) -> str:
    lines = ["推論ルール:"]
    for rule in rules:
        lines.append(f"  ・{rule.condition} → {rule.outcome}")
    return "\n".join(lines)


def _report_if_then_rules(rules: tuple[IfThenInferenceRule, ...]) -> list[str]:
    return [
        "推論ルール",
        *[f"  ・{rule.condition} → {rule.outcome}" for rule in rules],
        "",
    ]


def _format_inference_rules_block(template: WingPersonalityTemplate) -> str:
    parts: list[str] = []
    if template.inference_rules_if_then:
        parts.append(_format_if_then_rules(template.inference_rules_if_then))
    if template.inference_rules_map:
        title = (
            "推論ルール（分析・美学）"
            if template.inference_rules_if_then
            else "推論ルール"
        )
        parts.append(_format_dict_section(title, template.inference_rules_map))
    return "\n".join(parts)


def _format_tuple_values(title: str, items: tuple[str, ...]) -> str:
    lines = [f"{title}:"]
    lines.extend(f"  ・{item}" for item in items)
    return "\n".join(lines)


def _report_tuple_values(title: str, items: tuple[str, ...]) -> list[str]:
    return [title, *[f"  ・{item}" for item in items], ""]


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
    desc = _format_description(template)
    if template.decision_criteria:
        criteria_block = _format_dict_section("判断基準", template.decision_criteria)
        rules_block = _format_inference_rules_block(template)
        principles_block = _format_dict_section(
            "行動原理",
            template.behavioral_principles or {},
        )
        if template.value_profile_structured:
            values_block = _format_structured_values(template.value_profile_structured)
        elif template.value_profile_map:
            values_block = _format_value_profile_map(template.value_profile_map)
        elif template.value_profile:
            values_block = _format_tuple_values("価値プロフィール", template.value_profile)
        else:
            values_block = ""
        modules_block = (
            _format_additional_modules(template.additional_modules)
            if template.additional_modules
            else ""
        )
        archetype_block = _format_archetype_extension(template)
        body = "\n".join(
            part
            for part in (
                desc,
                criteria_block,
                rules_block,
                principles_block,
                values_block,
                modules_block,
                archetype_block,
            )
            if part
        )
    else:
        body = "\n".join(
            part
            for part in (
                desc,
                f"判断基準: {' / '.join(template.judgment_criteria)}",
                f"推論ルール: {' / '.join(template.inference_rules)}",
                f"行動原理: {' / '.join(template.behavior_principles)}",
                f"価値プロフィール: {' / '.join(template.value_profile)}",
            )
            if part
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
    if template.description:
        lines.extend(["概要", f"  {template.description}", ""])
    if template.decision_criteria:
        lines.extend(_report_dict_section("判断基準", template.decision_criteria))
        if template.inference_rules_if_then:
            lines.extend(_report_if_then_rules(template.inference_rules_if_then))
        if template.inference_rules_map:
            title = (
                "推論ルール（分析・美学）"
                if template.inference_rules_if_then
                else "推論ルール"
            )
            lines.extend(_report_dict_section(title, template.inference_rules_map))
        lines.extend(
            _report_dict_section("行動原理", template.behavioral_principles or {})
        )
        if template.value_profile_structured:
            lines.extend(_report_structured_values(template.value_profile_structured))
        elif template.value_profile_map:
            lines.extend(_report_dict_section("価値プロフィール", template.value_profile_map))
        elif template.value_profile:
            lines.extend(_report_tuple_values("価値プロフィール", template.value_profile))
        if template.additional_modules:
            lines.extend(
                _report_dict_section("追加モジュール", template.additional_modules)
            )
        lines.extend(_archetype_extension_report_lines(template))
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
    desc_html = (
        f"<p><em>{template.description}</em></p>" if template.description else ""
    )
    if template.decision_criteria:
        values_html = ""
        if template.value_profile_structured:
            for key, items in template.value_profile_structured.items():
                label = _VALUE_PROFILE_LABELS.get(key, key)
                values_html += f"<h5>{label}</h5><ul>{lis(items)}</ul>"
        elif template.value_profile_map:
            values_html = f"<ul>{lis_dict(template.value_profile_map)}</ul>"
        elif template.value_profile:
            values_html = f"<ul>{lis(template.value_profile)}</ul>"
        modules_html = ""
        if template.additional_modules:
            modules_html = f"""\
  <h4>追加モジュール</h4>
  <ul>{lis_dict(template.additional_modules)}</ul>"""
        archetype_html = ""
        if template.archetype_extension_name:
            archetype_html += f"<h4>アーキタイプ拡張: {template.archetype_extension_name}</h4>"
        if template.core_themes:
            archetype_html += f"""\
  <h4>コアテーマ</h4>
  <ul>{lis_dict(template.core_themes)}</ul>"""
        if template.archetypal_patterns:
            archetype_html += f"""\
  <h4>アーキタイプパターン</h4>
  <ul>{lis_dict(template.archetypal_patterns)}</ul>"""
        if template.inference_rules_if_then:
            rules_html = "".join(
                f"<li>{rule.condition} → {rule.outcome}</li>"
                for rule in template.inference_rules_if_then
            )
        else:
            rules_html = ""
        if template.inference_rules_map:
            map_rules_html = lis_dict(template.inference_rules_map)
            if template.inference_rules_if_then:
                rules_html += f"""\
  <h5>分析・美学</h5>
  <ul>{map_rules_html}</ul>"""
            else:
                rules_html = map_rules_html
        return f"""\
  <h3>ウイング人格: {header}</h3>
  {desc_html}
  <h4>判断基準</h4>
  <ul>{lis_dict(template.decision_criteria)}</ul>
  <h4>推論ルール</h4>
  <ul>{rules_html}</ul>
  <h4>行動原理</h4>
  <ul>{lis_dict(template.behavioral_principles or {})}</ul>
  <h4>価値プロフィール</h4>
  {values_html}
  {modules_html}
  {archetype_html}"""

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
