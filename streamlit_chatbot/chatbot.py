import streamlit as st
import google.generativeai as genai
import time
from PyPDF2 import PdfReader

# 🔐 Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAocTIF5SmA_A_INfLflAVRs9jxw22eT6w"
genai.configure(api_key=GOOGLE_API_KEY)

# Sidebar: Model Settings
with st.sidebar:
    st.title("⚙️ Settings")
    selected_model = st.selectbox("Choose model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7)
    use_context = st.toggle("🧠 Use Chat Context", value=True)
    uploaded_file = st.file_uploader("📄 Upload PDF or TXT", type=["pdf", "txt"])

# Load model
model = genai.GenerativeModel(selected_model)

# Read uploaded file (if any)
def read_uploaded_file(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        text = file.read().decode("utf-8")
    return text[:3000]

context_blob = read_uploaded_file(uploaded_file) if uploaded_file else ""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Get Gemini response
def get_gemini_response(prompt, context):
    full_prompt = f"{context}\nUser: {prompt}" if context else prompt
    response = model.generate_content(full_prompt, generation_config={"temperature": temperature})
    return response.text

# 🖌️ Blue theme CSS
def add_blue_theme():
    st.markdown("""
        <style>
            html, body {
                background-color: #e8f1fc;
                font-family: "Segoe UI", sans-serif;
            }
            .chat-bubble {
                padding: 12px 18px;
                border-radius: 12px;
                margin-bottom: 10px;
                font-size: 16px;
                max-width: 90%;
            }
            .user-msg {
                background-color: #d0ebff;
                color: #003366;
                align-self: flex-end;
            }
            .bot-msg {
                background-color: #cce5ff;
                color: #002855;
                align-self: flex-start;
            }
            .avatar {
                font-size: 20px;
                margin-right: 8px;
            }
            .stTitle {
                color: #1d4ed8;
            }
            button#mic {
                background-color: #60a5fa;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 8px;
                cursor: pointer;
            }
            .stButton>button {
                background-color: #2563eb;
                color: white;
                border-radius: 8px;
                padding: 0.5em 1em;
                margin-top: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

add_blue_theme()

# ✨ Typing simulation
def simulate_typing(message):
    placeholder = st.empty()
    for i in range(1, len(message) + 1):
        placeholder.markdown(f"<div class='chat-bubble bot-msg'><span class='avatar'>🤖</span>{message[:i]}</div>", unsafe_allow_html=True)
        time.sleep(0.01)

# Main UI
st.title("💙 Gemini AI Chatbot (Blue Edition)")

# Clear chat
if st.button("🔄 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat history
for msg in st.session_state.messages:
    role_icon = "👤" if msg["role"] == "user" else "🤖"
    css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-bubble {css_class}'><span class='avatar'>{role_icon}</span>{msg['content']}</div>", unsafe_allow_html=True)

# User prompt
if prompt := st.chat_input("💬 Ask something..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-bubble user-msg'><span class='avatar'>👤</span>{prompt}</div>", unsafe_allow_html=True)

    # Typing simulation and Gemini response
    with st.chat_message("assistant"):
        st.markdown("🤖 *Thinking...*")
        context = "\n".join([m["content"] for m in st.session_state.messages]) if use_context else ""
        if context_blob:
            context = context_blob + "\n" + context
        response = get_gemini_response(prompt, context)
        simulate_typing(response)

    # Store bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Feedback
    with st.expander("Did Gemini help you?"):
        col1, col2 = st.columns(2)
        with col1:
            st.button("👍 Yes", key=f"yes_{len(st.session_state.messages)}")
        with col2:
            st.button("👎 No", key=f"no_{len(st.session_state.messages)}")

# Optional voice input simulation button (HTML/JS simulation)
st.markdown("""
    <script>
        window.onload = function() {
            const mic = document.querySelector('#mic');
            if (mic) {
                mic.addEventListener('click', () => alert('🎙️ Voice input coming soon!'));
            }
        }
    </script>
    <button id="mic">🎙️ Voice</button>
""", unsafe_allow_html=True)
