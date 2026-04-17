    import streamlit as st
import requests
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="MyTeacher | Sovereign Edition", layout="wide")

def apply_styles():
    st.markdown("""
        <style>
        .main { background-color: #F8FAF8; }
        .kannada-card { 
            background-color: #FFFFFF; padding: 25px; border-radius: 12px; 
            border: 1px solid #E0E0E0; font-size: 1.4rem; line-height: 2.0; color: #1A237E;
        }
        .vocab-item {
            background-color: #FFFFFF; padding: 15px; border-radius: 10px; 
            margin-bottom: 12px; border: 1px solid #EEEEEE; color: #000000;
        }
        .vocab-word { color: #D32F2F; font-weight: bold; font-size: 1.1rem; }
        </style>
    """, unsafe_allow_html=True)

def call_sarvam_tts(text):
    """Actual API Call to Sarvam AI Bulbul v2"""
    url = "https://api.sarvam.ai/text-to-speech"
    
    payload = {
        "inputs": [text],
        "target_language_code": "kn-IN",
        "speaker": "meera",
        "model": "bulbul:v2",
        "pace": 0.8  # Pedagogical slow pace
    }
    
    headers = {
        "api-subscription-key": st.secrets["SARVAM_API_KEY"],
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            audio_base64 = response.json()['audios'][0]
            return base64.b64decode(audio_base64)
        else:
            st.error(f"Sarvam API Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Failed: {str(e)}")
        return None

# --- MOCK DATA ---
LESSON_DATA = {
    "content": "ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು.",
    "explanation": "This lesson introduces Dr. Rajendra Prasad. He was our first President and was loved for his humble nature.",
    "vocab": [
        {"word": "ಸರಳತೆ (Saralate)", "meaning": "Simplicity"},
        {"word": "ಸಜ್ಜನಿಕೆ (Sajjanike)", "meaning": "Nobility"}
    ]
}

def main():
    apply_styles()
    if 'reflection_submitted' not in st.session_state:
        st.session_state.reflection_submitted = False

    st.title("👨‍🏫 MyTeacher: Sovereign Edition")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<div class="kannada-card">{LESSON_DATA["content"]}</div>', unsafe_allow_html=True)
        with st.chat_message("teacher", avatar="👨‍🏫"):
            st.write(f"**Mentor:** {LESSON_DATA['explanation']}")
            
            if st.button("🔊 Play Lesson Narration"):
                audio_data = call_sarvam_tts(LESSON_DATA["content"])
                if audio_data:
                    st.audio(audio_data, format="audio/wav")

    with col2:
        st.subheader("📒 Alar Word Bank")
        for item in LESSON_DATA["vocab"]:
            st.markdown(f'<div class="vocab-item"><div class="vocab-word">{item["word"]}</div><div>{item["meaning"]}</div></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🤔 Holistic Reflection")
    user_thought = st.text_area("How would you stay simple like Rajendra Prasad?")
    
    if st.button("Submit Reflection"):
        if user_thought.strip():
            st.session_state.reflection_submitted = True
            st.balloons()

    if st.session_state.reflection_submitted:
        st.success("Great job! Now, let's review the difficult words.")
        st.subheader("🔊 Quick Word Review")
        
        for item in LESSON_DATA["vocab"]:
            with st.expander(f"Review: {item['word']}", expanded=True):
                st.write(f"**{item['word']}** means **{item['meaning']}**")
                if st.button(f"Hear '{item['word']}'", key=item['word']):
                    word_audio = call_sarvam_tts(f"{item['word']}. Meaning: {item['meaning']}")
                    if word_audio:
                        st.audio(word_audio, format="audio/wav")

if __name__ == "__main__":
    main()
