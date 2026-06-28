"""Tests for Gmail API email delivery."""

from unittest.mock import MagicMock, patch

import pytest

from sie.email.gmail import (
    GmailConfigError,
    send_enneagram_result_email,
    validate_email_address,
)
from sie.enneagram.profile import EnneagramProfile


def _sample_profile() -> EnneagramProfile:
    return EnneagramProfile(
        primary_type=1,
        wing=2,
        scores={1: 0.5},
        summary="summary",
        strengths=["a"],
        blind_spots=["b"],
        stress_pattern=4,
        growth_pattern=7,
        instinctual_variant="so",
        core_fear="fear",
        core_desire="desire",
        communication_style="style",
        conflict_pattern="conflict",
        relationship_needs=["need"],
        childhood_wound=None,
        episode_samples=[],
    )


def test_validate_email_address_accepts_valid() -> None:
    assert validate_email_address(" user@example.com ") == "user@example.com"


@pytest.mark.parametrize("address", ["", "not-an-email", "a@", "@b.com"])
def test_validate_email_address_rejects_invalid(address: str) -> None:
    with pytest.raises(ValueError, match="メールアドレス"):
        validate_email_address(address)


@patch.dict(
    "os.environ",
    {
        "GMAIL_CLIENT_ID": "id",
        "GMAIL_CLIENT_SECRET": "secret",
        "GMAIL_REFRESH_TOKEN": "refresh",
        "GMAIL_SENDER": "sender@gmail.com",
    },
)
@patch("sie.email.gmail.build")
@patch("sie.email.gmail._get_credentials")
def test_send_enneagram_result_email(mock_get_creds, mock_build) -> None:
    mock_service = MagicMock()
    mock_build.return_value = mock_service

    send_enneagram_result_email("recipient@example.com", _sample_profile())

    mock_service.users().messages().send.assert_called_once()
    call_kwargs = mock_service.users().messages().send.call_args.kwargs
    assert call_kwargs["userId"] == "me"
    assert "raw" in call_kwargs["body"]


@patch.dict("os.environ", {}, clear=True)
def test_send_enneagram_result_email_missing_config() -> None:
    with pytest.raises(GmailConfigError):
        send_enneagram_result_email("user@example.com", _sample_profile())
