"""One-time helper to obtain a Gmail API refresh token."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

from sie.email.gmail import GMAIL_SEND_SCOPE

load_dotenv()


def main() -> None:
    credentials_path = os.getenv(
        "GMAIL_CREDENTIALS_PATH",
        str(Path("credentials.json")),
    )
    if not Path(credentials_path).exists():
        raise SystemExit(
            f"credentials.json が見つかりません: {credentials_path}\n"
            "Google Cloud Console から OAuth クライアント ID をダウンロードし、"
            "プロジェクト直下に credentials.json として保存してください。"
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        scopes=[GMAIL_SEND_SCOPE],
    )
    creds = flow.run_local_server(port=0)

    print("\n以下を .env に追加してください:\n")
    print(f"GMAIL_CLIENT_ID={creds.client_id}")
    print(f"GMAIL_CLIENT_SECRET={creds.client_secret}")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
    print("GMAIL_SENDER=your@gmail.com")


if __name__ == "__main__":
    main()
