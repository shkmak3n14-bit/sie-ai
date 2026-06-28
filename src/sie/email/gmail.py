"""Send email via Gmail API."""

from __future__ import annotations

import base64
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sie.enneagram.profile import EnneagramProfile
from sie.enneagram.report import format_report_html, format_report_plain
from sie.enneagram.types import get_type_info

load_dotenv()

GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class GmailConfigError(ValueError):
    """Raised when Gmail API credentials are missing or invalid."""


def validate_email_address(address: str) -> str:
    """Validate and normalize an email address."""
    normalized = address.strip()
    if not normalized or not EMAIL_PATTERN.match(normalized):
        raise ValueError("有効なメールアドレスを入力してください。")
    return normalized


def _get_credentials() -> Credentials:
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise GmailConfigError(
            "Gmail API の設定が不足しています。"
            ".env に GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, "
            "GMAIL_REFRESH_TOKEN, GMAIL_SENDER を設定してください。"
        )

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=[GMAIL_SEND_SCOPE],
    )
    creds.refresh(Request())
    return creds


def _build_message(
    sender: str,
    to_address: str,
    subject: str,
    plain_body: str,
    html_body: str,
) -> dict[str, str]:
    message = MIMEMultipart("alternative")
    message["To"] = to_address
    message["From"] = sender
    message["Subject"] = subject
    message.attach(MIMEText(plain_body, "plain", "utf-8"))
    message.attach(MIMEText(html_body, "html", "utf-8"))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def send_enneagram_result_email(to_address: str, profile: EnneagramProfile) -> None:
    """Send the Enneagram assessment result to the given email address."""
    recipient = validate_email_address(to_address)
    sender = os.getenv("GMAIL_SENDER", "").strip()
    if not sender:
        raise GmailConfigError(
            "GMAIL_SENDER が設定されていません。.env に送信元 Gmail アドレスを設定してください。"
        )

    type_info = get_type_info(profile.primary_type)
    subject = f"S.I.E. エニアグラム診断結果 — {type_info.name}"
    plain_body = format_report_plain(profile)
    html_body = format_report_html(profile)

    try:
        service = build("gmail", "v1", credentials=_get_credentials(), cache_discovery=False)
        message = _build_message(sender, recipient, subject, plain_body, html_body)
        service.users().messages().send(userId="me", body=message).execute()
    except HttpError as exc:
        raise RuntimeError(f"Gmail API エラー: {exc}") from exc
