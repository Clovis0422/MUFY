import streamlit as st
import random

# ─── 100 Quotes for Each Category ───
def generate_quotes(category):
    endings = {
        "Inspiration": ["Be bold.", "Stay strong.", "Never give up.", "Shine bright.", "Embrace change."],
        "Wisdom": ["Knowledge is power.", "Think before you speak.", "Listen more.", "Be curious.", "Understand deeply."],
        "Humor": ["I'm not lazy, I'm energy-saving.", "Life's a joke—laugh.", "I’m not arguing, I’m explaining.", "Too cool for logic.", "Reality called—hung up."],
        "Life": ["Life goes on.", "Live and let live.", "Be present.", "Time flies.", "Change is constant."],
        "Success": ["Work smart.", "Push limits.", "Stay hungry.", "Dare greatly.", "Win with grace."]
    }
    return [f"{category} Quote #{i+1}: {random.choice(endings[category])}" for i in range(100)]

quotes = {cat: generate_quotes(cat) for cat in ["Inspiration", "Wisdom", "Humor", "Life", "Success"]}

# ─── Theme Styling ───
def inject_css(theme="light"):
    if theme == "light":
        bg_color, text_color, quote_bg = "#fdfcfb", "#333", "#fffdfc"
    else:
        bg_color, text_color, quote_bg = "#1e1e1e", "#f5f5f5", "#2c2c2c"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap');
    html, body {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Montserrat', sans-serif;
    }}
    .main > div {{
        max-width: 700px;
        margin: auto;
        padding: 2rem;
    }}
    .quote-box {{
        font-size: 1.4rem;
        padding: 2.5rem 2rem;
        margin-top: 2rem;
        background: {quote_bg};
        border-radius: 20px;
        position: relative;
        font-style: italic;
        text-align: center;
        animation: fadeIn 0.5s ease-in-out;
        box-shadow: inset 0 0 0 2px #ff7b54;
    }}
    .quote-box::before {{
        content: "❝";
        position: absolute;
        top: -20px;
        left: 20px;
        font-size: 5rem;
        color: rgba(255, 123, 84, 0.15);
    }}
    .quote-box::after {{
        content: "❞";
        position: absolute;
        bottom: -20px;
        right: 20px;
        font-size: 5rem;
        color: rgba(255, 123, 84, 0.15);
    }}
    .stButton>button {{
        background-color: #ff7b54;
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: #ff3e00;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ─── App Logic ───
def main():
    st.set_page_config(page_title="Fancy Quote Generator", layout="centered")

    if "favorites" not in st.session_state:
        st.session_state.favorites = []
    if "quote_key" not in st.session_state:
        st.session_state.quote_key = 0

    theme = st.radio("🌗 Theme", ["light", "dark"], horizontal=True)
    inject_css(theme)

    st.title("🌟 Fancy Quote Generator")

    category = st.selectbox("📚 Choose a Category", list(quotes.keys()))

    if st.button("🎲 Generate Quote"):
        st.session_state.quote_key = random.randint(0, 10000)

    random.seed(st.session_state.quote_key)
    current_quote = random.choice(quotes[category])
    quote_cleaned = current_quote.strip('"')

    st.markdown(f'<div class="quote-box">{quote_cleaned}</div>', unsafe_allow_html=True)

    if st.button("❤️ Save to Favorites"):
        if current_quote not in st.session_state.favorites:
            st.session_state.favorites.append(current_quote)
            st.success("Saved to favorites!")
        else:
            st.info("Already in favorites.")

    with st.expander("📔 View Favorites"):
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                st.markdown(f"<div class='quote-box'>{fav.strip('\"')}</div>", unsafe_allow_html=True)
        else:
            st.write("No favorites saved yet.")

# ─── Run ───
if __name__ == "__main__":
    main()
