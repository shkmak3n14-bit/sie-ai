"""Tests for separated confidence display."""

import pytest

pytest_plugins = ["tests.test_enneagram"]

from sie.enneagram.assess import run_assessment
from sie.enneagram.confidence import (
    format_confidence_lines,
    wing_confidence_detail,
)
from sie.enneagram.inputs import AssessmentInput


def test_wing_confidence_detail() -> None:
    conf, shares = wing_confidence_detail(7, 9, {"wing_low": 6.0, "wing_high": 2.0})
    assert conf == pytest.approx(0.75)
    assert shares[7] == pytest.approx(0.75)
    assert shares[9] == pytest.approx(0.25)


def test_format_confidence_lines_body_type8_w7(minimal_input: AssessmentInput) -> None:
    profile = run_assessment(minimal_input)
    lines = format_confidence_lines(profile)

    assert len(lines) == 3
    assert lines[0].startswith("センター信頼度：")
    assert "本能_" in lines[0] and "思考_" in lines[0] and "感情_" in lines[0]
    assert lines[1].startswith("主タイプ信頼度：")
    assert "8_" in lines[1] and "9_" in lines[1] and "1_" in lines[1]
    assert lines[2].startswith("ウイング信頼度：")
    assert "w7_" in lines[2] or "w9_" in lines[2]

    assert profile.center_confidence > 0
    assert profile.type_confidence > 0
    assert profile.wing_confidence >= 0
    assert set(profile.center_shares.keys()) == {"body", "heart", "head"}
    assert set(profile.type_shares_in_center.keys()) == {8, 9, 1}
