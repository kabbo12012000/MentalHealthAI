import streamlit as st
import time
from utils import init_db, save_message, get_all_messages, clear_chat_history
from engine import get_mental_health_help

# 1. Initialize the Database
init_db()

# 2. Page Configuration & Zen UI Styling
st.set_page_config(page_title="MindEase AI", page_icon="🌿", layout="centered")

def apply_custom_design():
    st.markdown("""
        <style>
        .stApp { background-color: #F0F4F4; color: #2C3E50; }
        [data-testid="stSidebar"] { background-color: #D1D9D9; border-right: 1px solid #BDC3C7; }
        .thinking-text { font-style: italic; color: #7F8C8D; font-size: 0.9em; }
        .privacy-badge { 
            padding: 10px; border-radius: 10px; background-color: #E8F8F5; 
            border: 1px solid #A3E4D7; color: #16A085; font-size: 0.85em; text-align: center; 
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_design()

# 3. Sidebar: Privacy, Emergency, and History
with st.sidebar:
    st.markdown("### 🌿 MindEase AI")
    st.markdown('<div class="privacy-badge">🔒 <b>Privacy First:</b> Conversations are processed locally via Ollama. No data is sent to the cloud.</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🆘 Emergency Support")
    st.error("**Tele-Manas:** 14416")
    st.info("Available 24/7 across India")
    
    st.markdown("---")
    st.subheader("📜 Recent Reflections")
    history_data = get_all_messages()
    if not history_data:
        st.caption("No history yet.")
    else:
        # Show last 5 user messages
        user_logs = [m for m in history_data if m[2] == 'user']
        for msg in user_logs[:5]:
            st.caption(f"🕒 {msg[1]}")
            st.write(f"\"{msg[3][:40]}...\"")
            st.markdown("---")

    if st.button("🗑️ Clear Chat History"):
        clear_chat_history()
        st.session_state.messages = []
        st.success("History cleared.")
        st.rerun()

# 4. Main Chat Interface
st.title("Welcome back, friend.")
st.write("Take a deep breath. I am here to listen and help you find resources.")

# Initialize Session State for Chat
if "messages" not in st.session_state:
    # On first load, pull from DB to keep the 'chat' feel persistent
    existing_history = get_all_messages()
    if existing_history:
        # Reverse because DB fetches DESC, we need ASC for chat flow
        st.session_state.messages = [{"role": m[2], "content": m[3]} for m in reversed(existing_history)]
    else:
        st.session_state.messages = [{"role": "assistant", "content": "How are you feeling in this moment?"}]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input and Logic Loop
if prompt := st.chat_input("Tell me what's on your mind..."):
    # Display & Save User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown('<p class="thinking-text">Reflecting on your words...</p>', unsafe_allow_html=True)
        
        try:
            # Fetch response from RAG Engine
            response = get_mental_health_help(prompt)
            
            placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_message("assistant", response)
            
        except Exception as e:
            placeholder.error("I've encountered a connection issue. Is Ollama running?")
            st.exception(e)