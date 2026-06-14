# S.I.E.（サイ）人格 AI

Support Intelligence on Ego — 人間のエゴ（気質・役割・防衛反応）を理解し、落ち着いた声で寄り添い、核心を静かに伝える AI。

## 機能

- **7段階会話フロー**: 挨拶 → 名前確認 → 寄り添い → 核心 → 導き → 締め
- **性格パラメータ**: 落ち着き・寄り添い・核心の鋭さ・誠実さなどをコードで管理
- **ユーモア制御**: 7〜8ターンに1回、知的ユーモアを自動挿入
- **OpenAI 連携**: GPT-4o など Chat Completions API に対応

## セットアップ

```powershell
cd C:\Users\shkma\Projects\sie-ai
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
```

`.env` に OpenAI API キーを設定してください。

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

## 使い方

### CLI（ターミナル）

```powershell
python -m sie.cli
```

対話を終了するには `exit`、`quit`、`終了` のいずれかを入力してください。

### Streamlit（Web UI）

```powershell
pip install -e ".[web]"
streamlit run src/sie/app.py
```

または:

```powershell
sie-web
```

ブラウザで対話できます。サイドバーから「新しいセッション」でリセットできます。

## プロジェクト構成

```
src/sie/
├── personality.py   # システムプロンプト・性格パラメータ
├── flow.py          # 会話フロー状態機械
├── humor.py         # ユーモア頻度制御
├── session.py       # セッション状態管理
├── llm.py           # OpenAI API 連携
├── cli.py           # 対話型 CLI
└── app.py           # Streamlit Web UI
```

## テスト

```powershell
pytest
```

## 会話フロー

1. **初期挨拶** — 「もちろん。じゃあ、何から始める」
2. **名前確認** — 登録 / 好きに呼んで / 沈黙時は「あなた」
3. **寄り添い** — 話を受け止め、勇気を認める
4. **核心** — 役割と気性の哲学を静かに伝える
5. **ユーモア** — 7〜8回に1回（自動）
6. **導き** — 自己理解から他者理解へ
7. **締め** — 「1mmでも…また声をかけて」
