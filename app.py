import streamlit as st
import requests
import base64
import time

# --- DESIGN SYSTEM: Slate & Indigo ---
st.set_page_config(page_title="Vernacular Learning Assistant", layout="wide", page_icon="📖")

def apply_enterprise_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+Kannada:wght@400;700&display=swap');
        
        /* Global Background & Typography */
        .main { background-color: #F9FAFB; font-family: 'Inter', sans-serif; }
        
        /* Heading */
        .main-title {
            color: #0F172A; font-size: 32px; font-weight: 700; text-align: center;
            margin-bottom: 40px; border-bottom: 2px solid #E2E8F0; padding-bottom: 10px;
        }

        /* Reader Area - 24px Font for Eye Clarity */
        .reader-card {
            background: white; padding: 45px; border-radius: 20px;
            border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            font-family: 'Noto Sans Kannada', sans-serif; font-size: 24px;
            line-height: 2.2; color: #1E293B; margin-bottom: 25px;
        }

        /* Narration Icon & Button */
        .stButton>button {
            background-color: #4F46E5; color: white; border-radius: 50px;
            padding: 15px 30px; font-weight: 600; border: none; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #4338CA; transform: scale(1.05); }

        /* Mastery Bank Cards */
        .mastery-card {
            background: #FFFFFF; border-radius: 12px; padding: 20px;
            border: 1px solid #F1F5F9; border-left: 6px solid #4F46E5;
            margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .word-kannada { font-family: 'Noto Sans Kannada', sans-serif; font-size: 22px; color: #4F46E5; font-weight: 700; }
        .meaning-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 5px; }
        .meaning-en { color: #1E293B; font-weight: 600; font-size: 14px; }
        .meaning-hi { color: #991B1B; font-weight: 600; font-size: 14px; }
        
        /* Usage Box */
        .usage-box {
            background: #F8FAFF; border: 1px dashed #CBD5E1; 
            padding: 12px; border-radius: 8px; margin-top: 10px;
        }
        .usage-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; }
        .usage-text { font-family: 'Noto Sans Kannada', sans-serif; font-size: 16px; margin-top: 4px; }
        </style>
    """, unsafe_allow_html=True)

# --- SARVAM TUTOR AUDIO ENGINE ---
def get_tutor_narration(verbatim_text, explanation):
    """Generates audio: Verbatim -> 1s Pause -> Tutor Explanation"""
    try:
        url = "https://api.sarvam.ai/text-to-speech"
        # The pause is simulated by punctuation and bridge phrasing
        full_script = f"{verbatim_text} ... ... ... ಈಗ ಇದರ ಅರ್ಥವನ್ನು ತಿಳಿಯೋಣ. {explanation}"
        
        payload = {
            "inputs": [full_script], "target_language_code": "kn-IN",
            "speaker": "meera", "model": "bulbul:v2", "pace": 0.82
        }
        headers = {"api-subscription-key": st.secrets["SARVAM_API_KEY"], "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return base64.b64decode(response.json()['audios'][0]) if response.status_code == 200 else None
    except:
        return None

# --- LESSON DATA REPOSITORY (POC MODE) ---
def fetch_lesson_content(para_index):
    # This structure ensures exactly 10 words per paragraph as per design specs
    paragraphs = [
        {
            "text": "ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು.",
            "tutor": "This introduces Dr. Rajendra Prasad. Notice how it highlights 'simplicity' and 'gentleness' as the core traits of a leader.",
            "words": [
                {"kn": "ಸರಳತೆ", "en": "Simplicity", "hi": "सादगी", "use": "ಗಾಂಧೀಜಿಯವರ ಸರಳತೆ ಮಾದರಿ."},
                {"kn": "ಸಜ್ಜನಿಕೆ", "en": "Gentleness", "hi": "सज्जनता", "use": "ಅವರ ಸಜ್ಜನಿಕೆ ನಮಗೆ ಇಷ್ಟ."},
                {"kn": "ರಾಷ್ಟ್ರಪತಿ", "en": "President", "hi": "राष्ट्रपति", "use": "ಅವರು ನಮ್ಮ ದೇಶದ ರಾಷ್ಟ್ರಪತಿ."},
                {"kn": "ಹೆಸರಾದವರು", "en": "Famous for", "hi": "प्रसिद्ध", "use": "ಅವರು ಒಳ್ಳೆಯ ಕೆಲಸಕ್ಕೆ ಹೆಸರಾದವರು."},
                {"kn": "ಮೊದಲ", "en": "First", "hi": "पहला", "use": "ಇದು ನಮ್ಮ ಮೊದಲ ಪಾಠ."},
                {"kn": "ಜೀವನ", "en": "Life", "hi": "जीवन", "use": "ಪ್ರಾಮಾಣಿಕ ಜೀವನ ನಡೆಸಿ."},
                {"kn": "ಗುಣ", "en": "Quality", "hi": "गुण", "use": "ವಿನಯ ಒಂದು ಒಳ್ಳೆಯ ಗುಣ."},
                {"kn": "ಭಾರತ", "en": "India", "hi": "भारत", "use": "ಭಾರತ ನಮ್ಮ ದೇಶ."},
                {"kn": "ವ್ಯಕ್ತಿತ್ವ", "en": "Personality", "hi": "व्यक्तित्व", "use": "ಅವರ ವ್ಯಕ್ತಿತ್ವ ಆಕರ್ಷಕ."},
                {"kn": "ಗೌರವ", "en": "Respect", "hi": "सम्मान", "use": "ಹಿರಿಯರಿಗೆ ಗೌರವ ನೀಡಿ."}
            ]
        },
        # Additional paragraphs (2-4) follow this exact 10-word mapping...
    ]
    # Default to Para 1 if out of range
    return paragraphs[para_index] if para_index < len(paragraphs) else paragraphs[0]

# --- UI ARCHITECTURE ---
def main():
    apply_enterprise_styles()
    
    if 'lesson_loaded' not in st.session_state:
        st.session_state.lesson_loaded = False
        st.session_state.current_para = 0

    st.markdown('<div class="main-title">Vernacular Learning Assistant</div>', unsafe_allow_html=True)

    # SIDEBAR: Control Plane
    with st.sidebar:
        st.subheader("📁 Lesson Source")
        url = st.text_input("Enter Lesson URL", placeholder="https://kannadakali.com/lesson1")
        if st.button("Load Lesson", use_container_width=True):
            st.session_state.lesson_loaded = True
            st.session_state.current_para = 0
            st.rerun()

        if st.session_state.lesson_loaded:
            st.divider()
            st.subheader("📍 Navigation")
            for i in range(4):
                if st.button(f"Paragraph {i+1}", key=f"nav_{i}", use_container_width=True):
                    st.session_state.current_para = i
                    st.rerun()

    # MAIN STAGE: Content Plane
    if st.session_state.lesson_loaded:
        data = fetch_lesson_content(st.session_state.current_para)
        col_reader, col_bank = st.columns([6, 4], gap="large")

        with col_reader:
            st.caption(f"READING WORKSPACE • PARAGRAPH {st.session_state.current_para + 1}")
            st.markdown(f'<div class="reader-card">{data["text"]}</div>', unsafe_allow_html=True)
            
            # Narration Hub
            c1, c2 = st.columns([1, 2])
            with c1:
                if st.button("🔊 Narrate Lesson"):
                    with st.spinner("Tutor preparing audio..."):
                        audio = get_tutor_narration(data["text"], data["tutor"])
                        if audio: st.audio(audio, format="audio/wav")
            
            with st.expander("📖 Personal Tutor Explanation", expanded=True):
                st.write(data["tutor"])

        with col_bank:
            st.caption("ALAR MASTERY BANK • 10 CORE WORDS")
            for word in data["words"]:
                st.markdown(f"""
                    <div class="mastery-card">
                        <div class="word-kannada">{word['kn']}</div>
                        <div class="meaning-grid">
                            <div class="meaning-en">EN: {word['en']}</div>
                            <div class="meaning-hi">HI: {word['hi']}</div>
                        </div>
                        <div class="usage-box">
                            <div class="usage-label">Contextual Usage</div>
                            <div class="usage-text">{word['use']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Please enter a lesson URL in the sidebar and click 'Load Lesson' to begin.")

if __name__ == "__main__":
    main()
