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
        "1w2", "2w1", "3w2", "3w4", "5w4", "7w6", "7w8", "8w7", "4w3", "4w5",
    }


def test_wing_type_code() -> None:
    assert wing_type_code(1, 2) == "1w2"
    assert wing_type_code(2, 1) == "2w1"
    assert wing_type_code(8, 7) == "8w7"
    assert wing_type_code(7, 8) == "7w8"
    assert wing_type_code(4, 3) == "4w3"
    assert wing_type_code(8, None) is None


def test_get_wing_template_lookup() -> None:
    template = get_wing_template(8, 7)
    assert template is not None
    assert template.label == "力 × 現実 × 責任"
    assert "不正・裏切りを最大の敵とみなす" in template.judgment_criteria


def test_get_wing_template_unknown_returns_none() -> None:
    assert get_wing_template(8, 9) is None
    assert get_wing_template(5, 6) is None


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


def test_7w6_fukumoto_template() -> None:
    template = get_wing_template(7, 6)
    assert template is not None
    assert template.model_name == "Fukumoto-Style_7w6"
    assert template.label == "刺激 × 楽観 × 忠誠"
    assert "退屈より刺激を優先する" in template.decision_criteria["stimulus_priority"]
    assert "likes" in template.value_profile_structured
    assert "退屈・停滞" in template.value_profile_structured["dislikes"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=7, wing=6)
    session.phase = ConversationPhase.CORE
    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "7w6" in instruction
    assert "Fukumoto-Style_7w6" in instruction
    assert "好む" in instruction
    assert "刺激で上書き" in instruction

    report = format_report_plain(_base_profile(primary_type=7, wing=6))
    assert "Fukumoto-Style_7w6" in report
    assert "尊敬する" in report


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
    assert template.model_name == "5w4_spirit_profile"
    assert template.version == "1.0"
    assert template.label == "契約 × 境界 × 静かな愛"
    assert "契約・原則・境界線" in template.decision_criteria["contract_priority"]
    assert template.inference_rules_if_then is not None
    assert len(template.inference_rules_if_then) == 6
    assert template.inference_rules_if_then[0].condition == "契約が破られた"
    assert "core_values" in template.value_profile_structured
    assert "愛によって壊れること" in template.value_profile_structured["fears"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=5, wing=4)
    session.phase = ConversationPhase.CORE
    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "5w4" in instruction
    assert "5w4_spirit_profile" in instruction
    assert "契約が破られた →" in instruction
    assert "コア価値" in instruction

    report = format_report_plain(_base_profile(primary_type=5, wing=4))
    assert "5w4_spirit_profile" in report
    assert "愛のスタイル" in report


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
    assert template.model_name == "Saint-Exupery_4w3_Profile"
    assert template.label == "喪失 × 自意識 × 美学"
    assert "本物か偽物か" in template.decision_criteria["inner_truth"]
    assert "象徴化し、詩的な物語へ" in template.inference_rules_map["rule_2_pain_to_symbol"]
    assert "深い共鳴" in template.behavioral_principles["principle_7_deep_resonance"]
    assert "本物の感情" in template.value_profile_structured["core_values"]
    assert "喪失の意味づけ" in template.value_profile_structured["desires"]

    session = Session.create()
    session.enneagram = _base_profile(primary_type=4, wing=3)
    session.phase = ConversationPhase.GUIDANCE

    instruction = get_enneagram_instruction(session)
    assert instruction is not None
    assert "4w3" in instruction
    assert "Saint-Exupery_4w3_Profile" in instruction
    assert "喪失 × 自意識 × 美学" in instruction
    assert "本物の感情" in instruction
    assert "寓話" in instruction


def test_report_includes_wing_template() -> None:
    profile = _base_profile(primary_type=7, wing=8)
    report = format_report_plain(profile)
    assert "7w8" in report
    assert "享楽 × 破滅 × 突破" in report
    assert "判断基準" in report
    assert "価値プロフィール" in report
