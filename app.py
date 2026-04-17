import streamlit as st
import requests
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="MyTeacher Pro", layout="wide", page_icon="👨‍🏫")

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Noto+Sans+Kannada:wght@400;700&display=swap');
        .main { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
        
        /* Reader Workspace */
        .reader-container {
            background: white; padding: 40px; border-radius: 24px;
            border: 1px solid #E2E8F0; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            font-family: 'Noto Sans Kannada', sans-serif; font-size: 1.7rem;
            line-height: 2.2; color: #1E293B; margin-bottom: 20px;
        }
        
        /* Contextual Word Cards */
        .alar-word-card {
            background: #FFFFFF; border-radius: 12px; padding: 18px;
            border: 1px solid #F1F5F9; border-left: 5px solid #4338CA;
            margin-bottom: 12px; transition: all 0.2s;
        }
        .alar-word-card:hover { border-left-width: 10px; background: #F8FAFF; }
        </style>
    """, unsafe_allow_html=True)

def call_sarvam_tts(text):
    """Bridges to Sarvam Bulbul v2 for high-quality pedagogical audio"""
    try:
        url = "https://api.sarvam.ai/text-to-speech"
        payload = {"inputs": [text], "target_language_code": "kn-IN", "speaker": "meera", "model": "bulbul:v2", "pace": 0.8}
        headers = {"api-subscription-key": st.secrets["SARVAM_API_KEY"], "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return base64.b64decode(response.json()['audios'][0])
    except:
        return None

# --- CORE SYSTEM DATA ---
LESSON_CONTENT = {
    "text": "ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು.",
    "explanation": "This paragraph introduces the values of India's first President. It emphasizes that true leadership comes from 'Saralate' (simplicity) and 'Sajjanike' (gentleness).",
    "vocab": [
        {"word": "ಸರಳತೆ (Saralate)", "meaning": "Simplicity", "usage": "ಗಾಂಧೀಜಿಯವರ ಸರಳತೆ ಮಾದರಿ.", "hi": "सादगी", "en_usage": "Gandhiji's simplicity is a model."},
        # Imagine 9 more words here...
    ]
}

def main():
    load_css()
    
    # 1. Lesson Entry (Bringing back URL/Input)
    with st.sidebar:
        st.title("👨‍🏫 Lesson Setup")
        lesson_url = st.text_input("Lesson URL", placeholder="https://kannadakali.com/lesson1")
        st.divider()
        st.success("Target: 6-Week POC Path")

    # 2. Hero Section
    st.markdown("<h1 style='color: #1A237E;'>Interactive Lesson Reader</h1>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([6, 4], gap="large")

    with col_left:
        st.subheader("📖 Text Analysis")
        st.markdown(f'<div class="reader-container">{LESSON_CONTENT["text"]}</div>', unsafe_allow_html=True)
        
        # Reader Controls
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Narrate & Explain"):
                # Combines verbatim readout with contextual explanation
                full_narration = f"{LESSON_CONTENT['text']}. Context: {LESSON_CONTENT['explanation']}"
                audio = call_sarvam_tts(full_narration)
                if audio: st.audio(audio, format="audio/wav")
        
        with c2:
            st.button("🎙️ Practice Reading (ASR)")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 Deep Contextual Meaning", expanded=True):
            st.write(LESSON_CONTENT["explanation"])

    with col_right:
        st.subheader("📒 Alar Mastery Bank (10 Words)")
        st.caption("Contextual usage and multi-lingual bridge")
        
        for item in LESSON_CONTENT["vocab"]:
            st.markdown(f"""
                <div class="alar-word-card">
                    <div style="color: #4338CA; font-weight: 700; font-size: 1.1rem;">{item['word']}</div>
                    <div style="color: #64748B; font-size: 0.9rem;">{item['meaning']} | {item['hi']}</div>
                    <div style="margin-top: 10px; background: #F1F5F9; padding: 8px; border-radius: 6px;">
                        <div style="font-size: 0.7rem; font-weight: 700; color: #94A3B8;">USAGE EXAMPLE</div>
                        <div style="font-size: 0.95rem; color: #1E293B;">{item['usage']}</div>
                        <div style="font-size: 0.8rem; font-style: italic; color: #64748B;">{item['en_usage']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
