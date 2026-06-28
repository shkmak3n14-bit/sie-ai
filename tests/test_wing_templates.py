"""Tests for wing personality templates."""

from sie.enneagram.context import get_enneagram_instruction
from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.report import format_report_plain
from sie.enneagram.wing_templates import (
    WING_TEMPLATES,
    get_wing_template,
    wing_type_code,
)
from sie.flow import ConversationPhase
from sie.session import Session


def _base_profile(**overrides) -> EnneagramProfile:
    defaults = dict(
        primary_type=8,
        wing=7,
        scores={n: 0.1 for n in range(1, 10)},
        summary="テスト",
        strengths=["力"],
        blind_spots=["支配"],
        stress_pattern=5,
        growth_pattern=2,
        instinctual_variant="sp",
        core_fear="弱さ",
        core_desire="力",
        communication_style="率直",
        conflict_pattern="正面",
        relationship_needs=["信頼"],
        childhood_wound="—",
        episode_samples=[],
    )
    defaults.update(overrides)
    return EnneagramProfile(**defaults)


def test_all_requested_templates_exist() -> None:
    assert set(WING_TEMPLATES) == {
        "1w2", "1w9", "2w1", "2w3", "3w2", "3w4", "5w4", "5w6", "6w5", "6w7", "7w6", "7w8", "8w7", "8w9", "9w1", "9w8", "4w3", "4w5",
    }


def test_wing_type_code() -> None:
    assert wing_type_code(1, 2) == "1w2"
    assert wing_type_code(1, 9) == "1w9"
    assert wing_type_code(2, 1) == "2w1"
    assert wing_type_code(2, 3) == "2w3"
    assert wing_type_code(6, 5) == "6w5"
    assert wing_type_code(6, 7) == "6w7"
    assert wing_type_code(8, 7) == "8w7"
    assert wing_type_code(8, 9) == "8w9"
    assert wing_type_code(9, 8) == "9w8"
    assert wing_type_code(9, 1) == "9w1"
    assert wing_type_code(7, 8) == "7w8"
    assert wing_type_code(4, 3) == "4w3"
    assert wing_type_code(8, None) is None


def test_get_wing_template_lookup() -> None:
    template = get_wing_template(8, 7)
    assert template is not None
    assert template.label == "力 × 現実 × 責任"
    assert "不正・裏切りを最大の敵とみなす" in template.judgment_criteria


def test_get_wing_template_unknown_returns_none() -> None:
    assert get_wing_template(8, 6) is None
    assert get_wing_template(2, 9) is None


def test_core_phase_includes_wing_template() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=8, wing=7)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "8w7" in instruction
    assert "力 × 現実 × 責任" in instruction
    assert "判断基準" in instruction
    assert "推論ルール" in instruction


def test_8w9_akio_template_in_instruction() -> None:
    template = get_wing_template(8, 9)
    assert template is not None
    assert template.model_name == "Akio_8w9"
    assert template.label == "構造 × 真実 × 調停"
    assert "感情パターン" in template.decision_criteria["structural_understanding"]
    assert "透明性" in template.decision_criteria["transparency_honesty"]
    assert "幼少期パターン" in template.inference_rules_map["internal_programs"]
    assert "個性を増幅" in template.inference_rules_map["positive_cycle_amplify"]
    assert "コミュニケーションを適応" in template.behavioral_principles["adapt_communication"]
    assert any("役割を超えて人間を理解" in item for item in template.value_profile)

    session = Session.create()
    session.enneagram = _base_profile(primary_type=8, wing=9)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "8w9" in instruction
    assert "Akio_8w9" in instruction
    assert "構造 × 真実 × 調停" in instruction
    assert "正 vs 負" in instruction
    assert "ユーモアで優しく触れる" in instruction
    assert "透明性は対立を減らし" in instruction

    report = format_report_plain(_base_profile(primary_type=8, wing=9))
    assert "8w9" in report
    assert "透明性と正直なコミュニケーション" in report


def test_9w8_template_in_instruction() -> None:
    template = get_wing_template(9, 8)
    assert template is not None
    assert template.label == "平和 × 本能 × 守護"
    assert "身体の奥で静かに燃える" in template.decision_criteria["quiet_anger"]
    assert "→ 9w8" in template.inference_rules_map["switch_overwhelming"]
    assert "腹が決まると一直線" in template.behavioral_principles["straight_line_resolve"]
    assert template.additional_modules is not None
    assert "9w1との対比（判断基準）" in template.additional_modules["contrast_judgment"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=9, wing=8)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "9w8" in instruction
    assert "平和 × 本能 × 守護" in instruction
    assert "スイッチが入ると圧倒的" in instruction
    assert "9w1との対比（行動）" in instruction

    report = format_report_plain(_base_profile(primary_type=9, wing=8))
    assert "9w8" in report
    assert "存在感を主張しない強さ" in report
    assert "平和 × 道徳" in report


def test_9w1_natsume_template() -> None:
    template = get_wing_template(9, 1)
    assert template is not None
    assert template.model_name == "Natsume_Takashi_9w1"
    assert template.label == "調和 × 共感 × 静かな倫理"
    assert "調和を保つ" in template.decision_criteria["harmony_maintenance"]
    assert "悪意より恐れ" in template.inference_rules_map["fear_not_malice"]
    assert "怒りから行動しない" in template.behavioral_principles["no_anger_action"]
    assert "natsume_core" in template.value_profile_structured
    assert "静かな倫理" in template.value_profile_structured["natsume_core"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=9, wing=1)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "9w1" in instruction
    assert "Natsume_Takashi_9w1" in instruction
    assert "調和 × 共感 × 静かな倫理" in instruction
    assert "最小限に介入" in instruction
    assert "運用原則" in instruction

    report = format_report_plain(_base_profile(primary_type=9, wing=1))
    assert "9w1" in report
    assert "選択の尊重" in report


def test_7w6_fukumoto_template() -> None:
    template = get_wing_template(7, 6)
    assert template is not None
    assert template.model_name == "Fukumoto-Style_7w6 + Father"
    assert template.label == "刺激 × 楽観 × 忠誠"
    assert "退屈より刺激を優先する" in template.decision_criteria["stimulus_priority"]
    assert "likes" in template.value_profile_structured
    assert "退屈・停滞" in template.value_profile_structured["dislikes"]
    assert "father_social_reputation" in template.decision_criteria
    assert "（Father）" in template.decision_criteria["father_family_dignity"]
    assert "father_profile" in template.value_profile_structured
    assert "社会的評判と面子" in template.value_profile_structured["father_profile"]
    assert "father_plan_collapse" in template.inference_rules_map
    assert "father_externalize" in template.behavioral_principles

    session = Session.create()
    session.enneagram = _base_profile(primary_type=7, wing=6)
    session.phase = ConversationPhase.CORE
    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "7w6" in instruction
    assert "Fukumoto-Style_7w6 + Father" in instruction
    assert "好む" in instruction
    assert "刺激で上書き" in instruction
    assert "Father" in instruction
    assert "理想化した未来のシナリオに固執する" in instruction
    assert "社会的評判と面子" in instruction

    report = format_report_plain(_base_profile(primary_type=7, wing=6))
    assert "Fukumoto-Style_7w6 + Father" in report
    assert "尊敬する" in report
    assert "失望は沈黙" in report


def test_3w2_senior_profile() -> None:
    template = get_wing_template(3, 2)
    assert template is not None
    assert template.model_name == "大学時代の先輩_3w2"
    assert template.label == "評価 × 好意 × 演じる自分"
    assert "好かれること" in template.inference_rules_map["likability_equals_value"]
    assert "電池切れ" in template.behavioral_principles["external_full_power_internal_shutdown"]
    assert "ショー化" in template.value_profile_structured["shadow_values"][3]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=3, wing=2)
    session.phase = ConversationPhase.CORE
    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "3w2" in instruction
    assert "大学時代の先輩_3w2" in instruction
    assert "肯定的価値" in instruction
    assert "影の側面" in instruction

    report = format_report_plain(_base_profile(primary_type=3, wing=2))
    assert "3w2" in report
    assert "演じる自分" in report


def test_3w4_boss_model_merged() -> None:
    template = get_wing_template(3, 4)
    assert template is not None
    assert template.model_name == "上司モデル_3w4"
    assert template.label == "達成者 × 個性派"
    assert "競争相手" in template.decision_criteria["competitor_threat"]
    assert "見捨てられる前兆" in template.inference_rules_map["loyalty_loss_as_abandonment"]
    assert "カメレオン的適応" in template.behavioral_principles["chameleon_advantage"]
    assert "成功している自分のイメージ" in template.value_profile

    session = Session.create()
    session.enneagram = _base_profile(primary_type=3, wing=4)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "3w4" in instruction
    assert "上司モデル_3w4" in instruction
    assert "達成者 × 個性派" in instruction
    assert "忖度" in instruction
    assert "存在価値の否定" in instruction

    report = format_report_plain(_base_profile(primary_type=3, wing=4))
    assert "3w4" in report
    assert "上司モデル" in report


def test_1w9_mother_template_in_instruction() -> None:
    template = get_wing_template(1, 9)
    assert template is not None
    assert template.model_name == "Mother_1w9"
    assert template.label == "道徳 × 調和 × 抑制"
    assert "あるべき姿" in template.decision_criteria["should_be_adherence"]
    assert "爆発的に放出" in template.inference_rules_map["anger_suppression_overflow"]
    assert "幼少期の混沌" in template.behavioral_principles["order_compensates_chaos"]
    assert "不必要でもタスクの完璧さ" in template.value_profile

    session = Session.create()
    session.enneagram = _base_profile(primary_type=1, wing=9)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "1w9" in instruction
    assert "Mother_1w9" in instruction
    assert "道徳 × 調和 × 抑制" in instruction
    assert "溢れるまで抑制され" in instruction
    assert "隠された行動は不正" in instruction
    assert "家族の調和" in instruction

    report = format_report_plain(_base_profile(primary_type=1, wing=9))
    assert "1w9" in report
    assert "直接対立を避け" in report
    assert "規則の厳守による安全" in report


def test_1w2_template_in_instruction() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=1, wing=2)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "1w2" in instruction
    assert "正義 × 献身 × 継承の義務" in instruction
    assert "正義の裏切り" in instruction
    assert "自己犠牲的な献身" in instruction

    report = format_report_plain(_base_profile(primary_type=1, wing=2))
    assert "1w2" in report
    assert "継承の義務" in report


def test_6w7_harry_potter_template() -> None:
    template = get_wing_template(6, 7)
    assert template is not None
    assert template.model_name == "Harry_Potter_6w7"
    assert template.label == "忠誠 × 警戒 × 希望"
    assert template.core_themes is not None
    assert "信じたいが疑う" in template.core_themes["loyalty_vs_doubt"]
    assert "言動の一貫性" in template.decision_criteria["trustworthiness"]
    assert "不安ループ" in template.inference_rules_map["anxiety_loop"]
    assert "軽さの仮面" in template.behavioral_principles["lightness_mask"]
    assert "loyalty_and_trust" in template.value_profile_structured
    assert "裏切り" in template.value_profile_structured["loyalty_and_trust"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=6, wing=7)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "6w7" in instruction
    assert "Harry_Potter_6w7" in instruction
    assert "忠誠 × 警戒 × 希望" in instruction
    assert "コアテーマ" in instruction
    assert "安全確保と冒険心の両立" in instruction
    assert "準備付き冒険" in instruction

    report = format_report_plain(_base_profile(primary_type=6, wing=7))
    assert "6w7" in report
    assert "恐怖を勇気の源に変換" in report


def test_6w5_template_in_instruction() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=6, wing=5)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "6w5" in instruction
    assert "演繹 × 忠誠 × 確実性" in instruction
    assert "演繹法を最上位の推論手段とする" in instruction
    assert "真実＝最大の善" in instruction

    report = format_report_plain(_base_profile(primary_type=6, wing=5))
    assert "6w5" in report
    assert "感情より理性" in report


def test_2w3_template_in_instruction() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=2, wing=3)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "2w3" in instruction
    assert "献身 × 適応 × 救済" in instruction
    assert "適応的再構築" in instruction
    assert "自己犠牲の美徳" in instruction

    report = format_report_plain(_base_profile(primary_type=2, wing=3))
    assert "2w3" in report
    assert "関係の修復と調和" in report


def test_2w1_template_in_instruction() -> None:
    session = Session.create()
    session.enneagram = _base_profile(primary_type=2, wing=1)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "2w1" in instruction
    assert "献身 × 義務 × 過剰な救済欲求" in instruction
    assert "救うための暴力" in instruction


def test_5w4_spirit_profile() -> None:
    template = get_wing_template(5, 4)
    assert template is not None
    assert template.model_name == (
        "5w4_spirit_profile + Jujutsu_5w4_Analytical_Aesthetic_Profile"
    )
    assert template.version == "1.0"
    assert template.label == "契約 × 境界 × 静かな愛"
    assert "契約・原則・境界線" in template.decision_criteria["contract_priority"]
    assert "rule_consistency" in template.decision_criteria
    assert "制約が強いほど美学的価値" in template.decision_criteria["constraint_beauty"]
    assert template.inference_rules_if_then is not None
    assert len(template.inference_rules_if_then) == 6
    assert template.inference_rules_if_then[0].condition == "契約が破られた"
    assert template.inference_rules_map is not None
    assert "条件分岐で整理" in template.inference_rules_map["rule_1_conditional_branching"]
    assert "core_values" in template.value_profile_structured
    assert "jujutsu_core_values" in template.value_profile_structured
    assert "制約の美学" in template.value_profile_structured["jujutsu_core_values"]
    assert "愛によって壊れること" in template.value_profile_structured["fears"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=5, wing=4)
    session.phase = ConversationPhase.CORE
    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "5w4" in instruction
    assert "Jujutsu_5w4_Analytical_Aesthetic_Profile" in instruction
    assert "契約が破られた →" in instruction
    assert "推論ルール（分析・美学）" in instruction
    assert "読み合いと戦略を優先" in instruction
    assert "コア価値" in instruction
    assert "分析・美学（コア価値）" in instruction

    report = format_report_plain(_base_profile(primary_type=5, wing=4))
    assert "Jujutsu_5w4_Analytical_Aesthetic_Profile" in report
    assert "愛のスタイル" in report
    assert "読み合いが成立しない状況" in report


def test_5w6_oreki_template() -> None:
    template = get_wing_template(5, 6)
    assert template is not None
    assert template.model_name == "Hyouka_5w6_Oreki"
    assert template.label == "氷菓型5w6（折木奉太郎モデル）"
    assert "最小化" in template.decision_criteria["energy_minimization"]
    assert "証拠を優先" in template.inference_rules_map["evidence_first"]
    assert "必要以上には関わらない" in template.behavioral_principles["limited_involvement"]
    assert template.additional_modules is not None
    assert "省エネ最適化" in template.additional_modules["core_logic"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=5, wing=6)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "5w6" in instruction
    assert "Hyouka_5w6_Oreki" in instruction
    assert "折木奉太郎" in instruction
    assert "本当に必要か" in instruction
    assert "追加モジュール" in instruction

    report = format_report_plain(_base_profile(primary_type=5, wing=6))
    assert "5w6" in report
    assert "必要なことだけを行う" in report


def test_4w5_deepsoul_template() -> None:
    template = get_wing_template(4, 5)
    assert template is not None
    assert template.model_name == "4w5_DeepSoul_Model"
    assert template.version == "1.0"
    assert template.label == "悲劇 × 永続 × 象徴 × 孤独"
    assert "永続性・宿命性" in template.decision_criteria["eternity_and_fate"]
    assert "表層→深層→根源" in template.inference_rules_map["three_layer_reasoning"]
    assert "破滅には導かない" in template.behavioral_principles["validate_without_ruin"]
    assert "孤独を欠陥ではなく" in template.value_profile_map["solitude_dignity"]
    assert "boundary_guard" in template.additional_modules
    assert template.archetype_extension_name == "4w5_Deep_Archetype_Extension"
    assert "宿命的関係性" in template.core_themes["eternal_bond"]
    assert "逃れられない関係性" in template.archetypal_patterns["fated_relationship"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=4, wing=5)
    session.phase = ConversationPhase.CORE
    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "4w5" in instruction
    assert "4w5_DeepSoul_Model" in instruction
    assert "追加モジュール" in instruction
    assert "象徴性・物語性" in instruction
    assert "Deep_Archetype_Extension" in instruction
    assert "コアテーマ" in instruction
    assert "美と残酷" in instruction

    report = format_report_plain(_base_profile(primary_type=4, wing=5))
    assert "DeepSoul" in report
    assert "追加モジュール" in report
    assert "アーキタイプ拡張" in report


def test_4w3_saint_exupery_merged_template() -> None:
    template = get_wing_template(4, 3)
    assert template is not None
    assert template.model_name == "Saint-Exupery_4w3_Profile + Brother"
    assert template.label == "喪失 × 自意識 × 美学"
    assert "本物か偽物か" in template.decision_criteria["inner_truth"]
    assert "象徴化し、詩的な物語へ" in template.inference_rules_map["rule_2_pain_to_symbol"]
    assert "深い共鳴" in template.behavioral_principles["principle_7_deep_resonance"]
    assert "本物の感情" in template.value_profile_structured["core_values"]
    assert "喪失の意味づけ" in template.value_profile_structured["desires"]
    assert "brother_comparative_identity" in template.decision_criteria
    assert "（Brother）" in template.decision_criteria["brother_comparative_identity"]
    assert "brother_freedom_from_norms" in template.decision_criteria
    assert "brother_conformity_threat" in template.inference_rules_map
    assert "brother_reject_should_norms" in template.behavioral_principles
    assert "brother_profile" in template.value_profile_structured
    assert "聖域としての孤独" in template.value_profile_structured["brother_profile"]
    assert "同調より真正性" in template.value_profile_structured["brother_profile"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=4, wing=3)
    session.phase = ConversationPhase.GUIDANCE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "4w3" in instruction
    assert "Saint-Exupery_4w3_Profile + Brother" in instruction
    assert "喪失 × 自意識 × 美学" in instruction
    assert "本物の感情" in instruction
    assert "寓話" in instruction
    assert "Brother" in instruction
    assert "個人的世界への退避" in instruction
    assert "同調より真正性" in instruction
    assert "あるべき」を拒む" in instruction


def test_7w8_adventurer_template() -> None:
    template = get_wing_template(7, 8)
    assert template is not None
    assert template.model_name == "攻めの知性・実験型冒険者 + 享楽×破滅×突破"
    assert template.label == "攻めの知性・実験型冒険者"
    assert "どれだけ楽しめるか" in template.decision_criteria["fun_maximization"]
    assert "legacy_boredom_enemy" in template.decision_criteria
    assert "（享楽×破滅×突破）" in template.decision_criteria["legacy_father_absence"]
    assert "失敗は素材" in template.inference_rules_map["failure_as_data"]
    assert "破滅の予兆があるほど" in template.inference_rules_map["legacy_ruin_pull"]
    assert "地獄を笑いながら突破" in template.behavioral_principles["enjoying_adversity"]
    assert "父性の代替を求める" in template.behavioral_principles["legacy_seek_father"]
    assert template.value_profile_map is not None
    assert "逆境を物語を面白くするスパイス" in template.value_profile_map["adversity_aesthetics"]
    assert "破滅の美学（享楽×破滅×突破）" in template.value_profile_map["legacy_ruin_aesthetics"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=7, wing=8)
    session.phase = ConversationPhase.CORE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "7w8" in instruction
    assert "攻めの知性・実験型冒険者 + 享楽×破滅×突破" in instruction
    assert "攻めの知性・実験型冒険者" in instruction
    assert "自力で突破できるルート" in instruction
    assert "試す・壊す・学ぶ" in instruction
    assert "享楽×破滅×突破" in instruction
    assert "喪失が起きると逃避または爆発" in instruction

    report = format_report_plain(_base_profile(primary_type=7, wing=8))
    assert "7w8" in report
    assert "判断基準" in report
    assert "新しい発見に価値を置く" in report
    assert "父性への潜在的渇望" in report


def test_report_includes_wing_template() -> None:
    profile = _base_profile(primary_type=7, wing=8)
    report = format_report_plain(profile)
    assert "7w8" in report
    assert "攻めの知性・実験型冒険者" in report
    assert "判断基準" in report
    assert "価値プロフィール" in report
