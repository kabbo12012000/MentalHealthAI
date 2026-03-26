import streamlit as st
import time
from engine import get_mental_health_help
from utils import clear_chat_history, get_all_messages, init_db, save_message

# Initialize the database immediately when the app starts
init_db()

# 1. Custom UI/UX Styling (The "Zen" Theme)
def apply_custom_design():
    st.markdown("""
        <style>
        /* Main background and font */
        .stApp {
            background-color: #F0F4F4; /* Soft Sage/Grey */
            color: #2C3E50;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #D1D9D9;
            border-right: 1px solid #BDC3C7;
        }

        /* Chat Input styling */
        .stChatInputContainer {
            padding-bottom: 20px;
        }

        /* Customizing the "Thinking" text */
        .thinking-text {
            font-style: italic;
            color: #7F8C8D;
            font-size: 0.9em;
        }

        /* Privacy Badge */
        .privacy-badge {
            padding: 10px;
            border-radius: 10px;
            background-color: #E8F8F5;
            border: 1px solid #A3E4D7;
            color: #16A085;
            font-size: 0.8em;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Page Configuration
st.set_page_config(page_title="MindEase AI", page_icon="🌿", layout="centered")
apply_custom_design()

# 3. Sidebar with Empathy-First Design
with st.sidebar:
    st.markdown("### 🌿 MindEase AI")
    st.markdown("---")
    st.markdown('<div class="privacy-badge">🔒 <b>Privacy First:</b> Your conversation is processed locally on your device via Ollama. No data is sent to the cloud.</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🆘 Emergency Support")
    st.error("**Tele-Manas:** 14416")
    st.info("Available 24/7 across India")
    
    if st.button("🗑️ Clear Chat History"):
        clear_chat_history()
        st.session_state.messages = []
        st.success("History wiped.")
        st.rerun()
    
    st.markdown("---")
    
    # 2. History Log
    st.subheader("📜 Recent Reflections")
    history = get_all_messages()
    
    if not history:
        st.write("No history yet. Start a conversation!")
    else:
        # We only show the last 5 user messages to keep it clean
        user_messages = [m for m in history if m[1] == 'user']
        for msg in user_messages[:5]:
            # This creates a small non-clickable text preview
            st.caption(f"🕒 {msg[0]}")
            st.write(f"\"{msg[2][:30]}...\"") # Shows the first 30 characters
            st.markdown("---")

# 4. Main Chat Interface
st.title("Welcome, friend.")

st.write("Take a deep breath. I am here to listen and help you find the right resources.")



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How are you feeling in this moment?"}]

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Chat Loop
if prompt := st.chat_input("Tell me what's on your mind..."):
    # Add user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Save user message to database
    save_message("user", prompt)
    # Assistant response with "Mindful Pause"
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown('<p class="thinking-text">Reflecting on your words...</p>', unsafe_allow_html=True)
        
        try:
            # Simulate a natural pause for "thinking"
            time.sleep(1) 
            
            # Fetch response from your RAG + Ollama Engine
            response = get_mental_health_help(prompt)
            
            placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            placeholder.error("I'm having a small technical hiccup. Please ensure Ollama is active.")