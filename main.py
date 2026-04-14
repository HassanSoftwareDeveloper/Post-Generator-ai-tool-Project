import streamlit as st
from few_shot import FewShotPosts
from text_generator import generate_post

length_options = ["Short", "Medium", "Long"]

language_options = [
    # Most widely used globally
    "English",
    "Mandarin Chinese",
    "Hindi",
    "Spanish",
    "French",
    "Arabic",
    "Bengali",
    "Portuguese",
    "Russian",
    "Urdu",

    # European
    "German",
    "Italian",
    "Dutch",
    "Polish",
    "Swedish",
    "Norwegian",
    "Danish",
    "Finnish",
    "Greek",
    "Czech",
    "Romanian",
    "Hungarian",
    "Slovak",
    "Bulgarian",
    "Croatian",
    "Serbian",
    "Ukrainian",
    "Catalan",
    "Turkish",

    # South & Southeast Asian
    "Indonesian",
    "Malay",
    "Tamil",
    "Telugu",
    "Marathi",
    "Gujarati",
    "Kannada",
    "Malayalam",
    "Punjabi",
    "Sinhala",
    "Nepali",
    "Thai",
    "Vietnamese",
    "Filipino (Tagalog)",
    "Burmese",
    "Khmer",

    # East Asian
    "Japanese",
    "Korean",
    "Traditional Chinese",

    # Middle Eastern & African
    "Persian (Farsi)",
    "Hebrew",
    "Swahili",
    "Amharic",
    "Hausa",
    "Yoruba",
    "Zulu",
    "Afrikaans",

    # Latin American
    "Mexican Spanish",
    "Brazilian Portuguese",

    # Mixed / Informal
    "Hinglish (Hindi + English)",
    "Spanglish (Spanish + English)",
]

tone_options = [
    # Authority & Thought Leadership
    "Professional",
    "Expert Opinion",
    "Teach Me Something",
    "Facts & Numbers",
    "Straight to the Point",

    # Personal & Emotional
    "Uplifting",
    "Tell a Story",
    "Real & Honest",
    "Push Me to Act",
    "I Understand You",

    # Conversational & Engaging
    "Chill & Friendly",
    "Just Talking",
    "Clever & Witty",
    "Make Me Laugh",
    "Feels Like Me",

    # Action & Value Oriented
    "Bold & Controversial",
    "My Strong Opinion",
    "Here's the Problem & Fix",
    "Step by Step",
    "Quick List",

    # Niche & Advanced
    "Short & Powerful",
    "Poetic",
    "What's Trending",
    "Behind the Scenes",
    "Take Action Now",
]

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Soft dark navy — not pure black, warm enough for long reading */
    .stApp {
        background: #1c1e2e;
    }

    /* Constrain content width for readability on wide layout */
    .block-container {
        max-width: 860px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin: 0 auto !important;
    }

    /* ── Hero ── */
    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: rgba(124, 106, 247, 0.12);
        border: 1px solid rgba(124, 106, 247, 0.28);
        color: #b0a4f8;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        padding: 0.38rem 1rem;
        border-radius: 20px;
        margin-bottom: 1.3rem;
    }

    .hero-badge::before {
        content: '';
        width: 6px;
        height: 6px;
        background: #7c6af7;
        border-radius: 50%;
        box-shadow: 0 0 7px rgba(124,106,247,0.8);
    }

    .hero-title {
        font-size: 2.9rem;
        font-weight: 800;
        color: #e8eaf0;
        line-height: 1.12;
        margin-bottom: 0.9rem;
        letter-spacing: -0.025em;
    }

    .hero-title span {
        background: linear-gradient(135deg, #7c6af7 0%, #a78bfa 60%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #9096b0;
        font-weight: 400;
        max-width: 430px;
        margin: 0 auto 1.8rem;
        line-height: 1.75;
    }

    /* ── Stats row ── */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-bottom: 2.2rem;
    }

    .stat-item { text-align: center; }

    .stat-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #d4d7e8;
        letter-spacing: -0.02em;
    }

    .stat-label {
        font-size: 0.7rem;
        color: #5c6280;
        font-weight: 500;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-top: 0.15rem;
    }

    /* ── Form card ── */
    .form-card {
        background: #242638;
        border: 1px solid #2e3148;
        border-radius: 18px;
        padding: 1.8rem 1.8rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 24px rgba(0,0,0,0.25);
        position: relative;
        overflow: hidden;
    }

    .form-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124,106,247,0.45), transparent);
    }

    .form-card-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #5c6280;
        margin-bottom: 1.1rem;
    }

    /* ── Text input ── */
    .stTextInput > div > div > input {
        background-color: #1c1e2e !important;
        border: 1px solid #2e3148 !important;
        border-radius: 10px !important;
        color: #d4d7e8 !important;
        font-size: 0.93rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        padding: 0.55rem 0.85rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7c6af7 !important;
        box-shadow: 0 0 0 3px rgba(124,106,247,0.1) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #3e4460 !important;
    }
    .stTextInput label {
        color: #7a80a0 !important;
        font-size: 0.77rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }
    .stSelectbox > div > div {
        background-color: #1c1e2e !important;
        border: 1px solid #2e3148 !important;
        border-radius: 10px !important;
        color: #d4d7e8 !important;
        font-size: 0.93rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }

    .stSelectbox > div > div:hover {
        border-color: #7c6af7 !important;
        box-shadow: 0 0 0 3px rgba(124,106,247,0.1) !important;
    }

    .stSelectbox label {
        color: #7a80a0 !important;
        font-size: 0.77rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    /* ── Generate button ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #7c6af7 0%, #9b59f5 100%);
        color: #ffffff;
        border: none;
        border-radius: 11px;
        padding: 0.85rem 2rem;
        font-size: 0.96rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        cursor: pointer;
        transition: all 0.22s ease;
        box-shadow: 0 4px 18px rgba(124,106,247,0.28);
        margin-top: 0.7rem;
    }

    .stButton > button:hover {
        box-shadow: 0 6px 28px rgba(124,106,247,0.42);
        transform: translateY(-1px);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 10px rgba(124,106,247,0.2);
    }

    /* ── Output card ── */
    .output-card {
        background: #242638;
        border: 1px solid #2e3148;
        border-radius: 18px;
        padding: 1.5rem 1.8rem 1rem;
        margin-top: 1.2rem;
        box-shadow: 0 2px 24px rgba(0,0,0,0.25);
        position: relative;
        overflow: hidden;
    }

    .output-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
    }

    .output-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .output-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #5c6280;
    }

    .output-tag {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #a78bfa;
        background: rgba(167,139,250,0.1);
        border: 1px solid rgba(167,139,250,0.22);
        padding: 0.22rem 0.65rem;
        border-radius: 6px;
    }

    /* ── Textarea — warm readable background ── */
    .stTextArea > div > div > textarea {
        background-color: #1c1e2e !important;
        border: 1px solid #2e3148 !important;
        border-radius: 10px !important;
        color: #dde0ee !important;          /* warm off-white, easy on eyes */
        font-size: 0.96rem !important;
        line-height: 1.85 !important;       /* generous line height for reading */
        font-family: 'Inter', sans-serif !important;
        padding: 1rem 1.2rem !important;
        caret-color: #7c6af7 !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #7c6af7 !important;
        box-shadow: 0 0 0 3px rgba(124,106,247,0.12) !important;
        outline: none !important;
    }

    .output-hint {
        font-size: 0.71rem;
        color: #4a5070;
        margin-top: 0.55rem;
        text-align: right;
        letter-spacing: 0.02em;
    }

    /* ── Hashtag block ── */
    .hashtag-block {
        margin-top: 0.8rem;
        padding: 0.75rem 1rem;
        background: rgba(124, 106, 247, 0.07);
        border: 1px solid rgba(124, 106, 247, 0.18);
        border-radius: 10px;
        color: #9b8ff5;
        font-size: 0.88rem;
        font-weight: 500;
        line-height: 1.8;
        letter-spacing: 0.01em;
        word-spacing: 0.4rem;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #7c6af7 !important; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #1c1e2e; }
    ::-webkit-scrollbar-thumb { background: #2e3148; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #7c6af7; }

    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="LinkedIn Post Generator",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    apply_styles()

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">AI-Powered Content Studio</div>
        <div class="hero-title"> Posts<br><span>Generator</span></div>
        <div class="hero-subtitle">
            Pick a topic, choose your tone, and get a ready-to-post
            write-up in seconds — in any language, any style.
        </div>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">100+</div>
                <div class="stat-label">Topics</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">25</div>
                <div class="stat-label">Tone Styles</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">60+</div>
                <div class="stat-label">Languages</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">AI</div>
                <div class="stat-label">Few-Shot</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fs = FewShotPosts()

    st.markdown('<div class="form-card"><div class="form-card-title">Configure your post</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_tag = st.text_input("Topic", placeholder="e.g. Burnout at work, AI replacing jobs, Morning routines...")
        selected_length = st.selectbox("Length", options=length_options)
    with col2:
        selected_tone = st.selectbox("Tone", options=tone_options)
        selected_language = st.selectbox("Language", options=language_options)

    generate_clicked = st.button("Generate Post", disabled=not selected_tag.strip())
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_clicked:
        with st.spinner("Crafting your post..."):
            post = generate_post(selected_length, selected_language, selected_tag, selected_tone)

        # Split post body and hashtags
        lines = post.strip().split('\n')
        hashtag_line = ""
        body_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') and all(w.startswith('#') for w in stripped.split()):
                hashtag_line = stripped
            else:
                body_lines.append(line)

        post_body = '\n'.join(body_lines).strip()
        hashtags = hashtag_line.strip()

        st.markdown(f"""
        <div class="output-card">
            <div class="output-header">
                <div class="output-title">Generated Post</div>
                <div class="output-tag">{selected_tone} &middot; {selected_length}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.text_area("", value=post_body, height=420, key="final_output", label_visibility="collapsed")

        if hashtags:
            st.markdown(f'<div class="hashtag-block">{hashtags}</div>', unsafe_allow_html=True)

        st.markdown('<div class="output-hint">Click inside the box &nbsp;·&nbsp; Ctrl+A to select &nbsp;·&nbsp; Ctrl+C to copy</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
