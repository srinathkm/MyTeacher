import streamlit as st
import requests
import base64
import random

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="MyTeacher Pro | Dynamic Learner", layout="wide", page_icon="👨‍🏫")

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Noto+Sans+Kannada:wght@400;700&display=swap');
        .main { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
        
        /* Glassmorphism Sidebar */
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
        
        /* Enterprise Reader Card */
        .reader-container {
            background: white; padding: 40px; border-radius: 24px;
            border: 1px solid #E2E8F0; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            font-family: 'Noto Sans Kannada', sans-serif; font-size: 1.8rem;
            line-height: 2.3; color: #1E293B; margin-bottom: 20px;
        }
        
        /* Master Word Cards */
        .alar-card {
            background: #FFFFFF; border-radius: 12px; padding: 18px;
            border: 1px solid #F1F5F9; border-left: 5px solid #4338CA;
            margin-bottom: 12px; transition: all 0.2s;
        }
        .alar-card:hover { transform: translateY(-2px); border-left-width: 10px; }
        .usage-box { background: #F8FAFF; padding: 10px; border-radius: 8px; margin-top: 10px; border: 1px dashed #CBD5E1; }
        </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC: SARVAM TTS ---
def call_sarvam_tts(text):
    try:
        url = "https://api.sarvam.ai/text-to-speech"
        payload = {
            "inputs": [text],
            "target_language_code": "kn-IN",
            "speaker": "meera",
            "model": "bulbul:v2",
            "pace": 0.85
        }
        headers = {"api-subscription-key": st.secrets["SARVAM_API_KEY"], "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return base64.b64decode(response.json()['audios'][0])
    except:
        return None

# --- MOCK EXTRACTOR (POC MODE) ---
# This simulates what Alar/Gemini would extract from a fresh URL
def get_lesson_data(url, paragraph_index):
    # In a real POC, this would scrape the URL. Here we provide the logic for the 1st Lesson.
    paragraphs = [
        "ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು.",
        "ಒಮ್ಮೆ ಅವರು ರೈಲು ನಿಲ್ದಾಣದಲ್ಲಿ ಸಾಮಾನ್ಯ ಮನುಷ್ಯನಂತೆ ಕುಳಿತಿದ್ದರು. ಯಾರೂ ಅವರನ್ನು ಗುರುತಿಸಲಿಲ್ಲ.",
        "ನಿಲ್ದಾಣದ ಅಧಿಕಾರಿ ಬಂದು ಅವರನ್ನು ವಿಚಾರಿಸಿದಾಗ, ಅವರು ವಿನಯದಿಂದ ಉತ್ತರ ನೀಡಿದರು.",
        "ಅವರ ಜೀವನದ ಈ ಘಟನೆ ನಮಗೆ ದೊಡ್ಡ ಪಾಠವನ್ನು ಕಲಿಸುತ್ತದೆ. ಅಧಿಕಾರವಿದ್ದರೂ ಸರಳವಾಗಿರಬೇಕು."
    ]
    
    # Dynamic 10-word bank generation logic
    all_words = [
        {"w": "ಸರಳತೆ", "m": "Simplicity", "u": "ಸರಳತೆ ಶ್ರೇಷ್ಠ ಗುಣ.", "h": "सादगी", "e": "Simplicity is a great virtue."},
        {"w": "ಸಜ್ಜನಿಕೆ", "m": "Gentleness", "u": "ಅವರಲ್ಲಿ ಸಜ್ಜನಿಕೆ ಇದೆ.", "h": "सज्जनता", "e": "He has gentleness in him."},
        {"w": "ಗುರುತಿಸು", "m": "Identify", "u": "ನಾನು ನಿನ್ನನ್ನು ಗುರುತಿಸಿದೆ.", "h": "पहचानना", "e": "I recognized you."},
        {"w": "ವಿನಯ", "m": "Humility", "u": "ವಿನಯದಿಂದ ಮಾತನಾಡು.", "h": "विनम्रता", "e": "Speak with humility."},
        {"w": "ಅಧಿಕಾರ", "m": "Power/Authority", "u": "ಅಧಿಕಾರ ಸಿಕ್ಕಾಗ ಮದ ಬರಬಾರದು.", "h": "अधिकार", "e": "Power shouldn't bring ego."},
        {"w": "ಘಟನೆ", "m": "Incident", "u": "ಇದು ನಡೆದ ನಿಜವಾದ ಘಟನೆ.", "h": "घटना", "e": "This is a true incident."},
        {"w": "ವಿಚಾರಿಸು", "m": "Inquire", "u": "ಕ್ಷೇಮವನ್ನು ವಿಚಾರಿಸು.", "h": "पूछना", "e": "Inquire about well-being."},
        {"w": "ಸಾಮಾನ್ಯ", "m": "Common/Ordinary", "u": "ಅವನು ಸಾಮಾನ್ಯ ಮನುಷ್ಯ.", "h": "सामान्य", "e": "He is a common man."},
        {"w": "ಸೇವೆ", "m": "Service", "u": "ಜನರ ಸೇವೆ ಮಾಡಿ.", "h": "सेवा", "e": "Do service for people."},
        {"w": "ಆದರ್ಶ", "m": "Ideal", "u": "ಇದು ಒಂದು ಆದರ್ಶ ಶಾಲಾ.", "h": "आदर्श", "e": "This is an ideal school."}
    ]
    
    return paragraphs[paragraph_index], all_words

# --- UI RENDERER ---
def main():
    load_css()
    
    # 1. Sidebar for URL and POC Nav
    with st.sidebar:
        st.title("👨‍🏫 POC Setup")
        lesson_url = st.text_input("Enter Lesson URL", value="https://example.com/kannada-lesson-1")
        st.divider()
        st.write("### Paragraph Navigator")
        para_idx = st.radio("Select Paragraph", options=[0, 1, 2, 3], format_func=lambda x: f"Paragraph {x+1}")
        st.info("The app will extract 10 words from every paragraph automatically.")

    # 2. Main Workspace
    text, words = get_lesson_data(lesson_url, para_idx)
    
    st.markdown(f"<h1 style='color: #1A237E;'>Sovereign Reader: Paragraph {para_idx + 1}</h1>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([6, 4], gap="large")

    with col_left:
        st.markdown(f'<div class="reader-container">{text}</div>', unsafe_allow_html=True)
        
        # Reader Actions
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Narrate & Explain"):
                explanation = f"Paragraph {para_idx + 1} of the lesson. The content is: {text}. Key takeaway: Focus on values over status."
                audio = call_sarvam_tts(explanation)
                if audio: st.audio(audio, format="audio/wav")
        
        with c2:
            st.button("🎙️ Voice Practice")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📝 Contextual Exercise")
        st.write("Pick a word from the right and use it in your own sentence below:")
        st.text_input("My Sentence Construction:", key=f"user_input_{para_idx}")

    with col_right:
        st.subheader(f"📒 Alar Mastery Bank (10 Words)")
        st.caption("Contextual meanings with Hindi/English bridges")
        
        # Render exactly 10 words
        for item in words:
            st.markdown(f"""
                <div class="alar-card">
                    <div style="color: #4338CA; font-weight: 700; font-size: 1.1rem;">{item['w']}</div>
                    <div style="color: #64748B; font-size: 0.9rem;">{item['m']} | {item['h']}</div>
                    <div class="usage-box">
                        <div style="font-size: 0.7rem; font-weight: 700; color: #94A3B8;">KANNADA USAGE</div>
                        <div style="font-size: 0.95rem; color: #1E293B; font-weight: 600;">{item['u']}</div>
                        <div style="font-size: 0.85rem; font-style: italic; color: #64748B;">{item['e']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
