import streamlit as st
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="MyTeacher | Sovereign Edition", layout="wide")

def apply_styles():
    st.markdown("""
        <style>
        .main { background-color: #F8FAF8; }
        .kannada-card { 
            background-color: #FFFFFF; 
            padding: 25px; 
            border-radius: 12px; 
            border: 1px solid #E0E0E0;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            font-size: 1.4rem;
            line-height: 2.0;
            color: #1A237E;
            margin-bottom: 20px;
        }
        /* Alar Link Card Redesign - White background, black text for clarity */
        .vocab-item {
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 12px;
            border: 1px solid #EEEEEE;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
            color: #000000;
        }
        .vocab-word {
            color: #D32F2F; /* Red accent for the word */
            font-weight: bold;
            font-size: 1.1rem;
        }
        .vocab-meaning {
            color: #212121;
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# Mock function for Sarvam TTS (Placeholder for actual API)
def get_audio_placeholder():
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# --- MOCK DATA ---
LESSON_DATA = {
    "title": "Lesson 1: Dr. Rajendra Prasad",
    "content": "ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು.",
    "explanation": "This lesson introduces Dr. Rajendra Prasad. He was our first President and was loved for his humble nature.",
    "vocab": [
        {"word": "ಸರಳತೆ (Saralate)", "meaning": "Simplicity", "usage": "Living a life without luxury, even when powerful."},
        {"word": "ಸಜ್ಜನಿಕೆ (Sajjanike)", "meaning": "Nobility", "usage": "Being a true gentleman to everyone."}
    ]
}

def main():
    apply_styles()
    
    # Initialize session state for logic triggers
    if 'reflection_submitted' not in st.session_state:
        st.session_state.reflection_submitted = False

    st.title("👨‍🏫 MyTeacher: Sovereign Edition")
    st.caption("Native Kannada Learning Stack (Sarvam AI + Alar.ink)")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<div class="kannada-card">{LESSON_DATA["content"]}</div>', unsafe_allow_html=True)
        
        with st.chat_message("teacher", avatar="👨‍🏫"):
            st.write(f"**Mentor:** {LESSON_DATA['explanation']}")
            st.audio(get_audio_placeholder())
            st.caption("🔊 Lesson Narration (Powered by Sarvam Shunya)")

    with col2:
        st.subheader("📒 Alar Word Bank")
        for item in LESSON_DATA["vocab"]:
            st.markdown(f"""
                <div class="vocab-item">
                    <div class="vocab-word">{item['word']}</div>
                    <div class="vocab-meaning"><b>Meaning:</b> {item['meaning']}</div>
                    <div style='font-size: 0.9rem; color: #616161;'>{item['usage']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()
    
    # Reflection Section
    st.subheader("🤔 Holistic Reflection")
    st.write("If you were a leader like Rajendra Prasad, how would you stay simple?")
    user_thought = st.text_area("Your thoughts:", placeholder="Type or speak your summary here...")
    
    if st.button("Submit Reflection"):
        if user_thought.strip():
            st.session_state.reflection_submitted = True
        else:
            st.warning("Please share your thoughts before submitting!")

    # Post-submission feedback and Vocabulary Hear-back logic
    if st.session_state.reflection_submitted:
        st.balloons()
        st.success("Wonderful reflection! You've captured the heart of the lesson.")
        
        st.markdown("---")
        st.subheader("🔊 Quick Word Review")
        st.write("Listen to the key words from this lesson one more time to remember them:")
        
        for item in LESSON_DATA["vocab"]:
            with st.expander(f"Hear: {item['word']}", expanded=True):
                st.write(f"**{item['word']}** - {item['meaning']}")
                # In production, this would be an individual API call to Sarvam TTS for the word
                st.audio(get_audio_placeholder())
                st.caption(f"Reviewing pronunciation: {item['word']}")
        
        if st.button("Start Next Lesson"):
            st.session_state.reflection_submitted = False
            st.rerun()

if __name__ == "__main__":
    main()
