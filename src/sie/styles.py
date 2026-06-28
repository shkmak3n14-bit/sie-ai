"""Shared Streamlit CSS for S.I.E."""

APP_CSS = """
<style>
.stApp {
    background: linear-gradient(180deg, #0f1419 0%, #1a2332 100%);
    color: #e8eef4;
}
.stApp p, .stApp span, .stApp label, .stApp li, .stApp div {
    color: #e8eef4;
}
[data-testid="stSidebar"] {
    background-color: #151d28;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #e8eef4;
}
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 0.5rem;
}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] span,
[data-testid="stChatMessageContent"] li {
    color: #f5f8fc;
}
[data-testid="stCaptionContainer"] p {
    color: #a8bccf;
}
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"] > div {
    background-color: #0f1419;
}

/* White-background inputs: force dark text (overrides global light text) */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input,
[data-testid="stChatInput"] textarea {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background-color: #ffffff !important;
    caret-color: #000000;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stNumberInput"] input::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(0, 0, 0, 0.45) !important;
    -webkit-text-fill-color: rgba(0, 0, 0, 0.45) !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
.stApp [data-baseweb="input"] input,
.stApp [data-baseweb="textarea"] {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #000000;
}
[data-testid="stChatInput"] {
    background-color: #ffffff;
    border-color: #cccccc;
    color: #000000;
    caret-color: #000000;
}
[data-testid="stChatInput"] button {
    color: #000000;
}
h1 { color: #b8d4f0; font-weight: 300; }
h2 { color: #c8dff5; font-weight: 300; }
h3 { color: #c8dff5; }
.sie-caption { color: #a8bccf; font-size: 0.9rem; }
.enneagram-result {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
</style>
"""
