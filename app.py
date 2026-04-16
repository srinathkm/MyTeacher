import streamlit as st
import time
import requests

# --- CONFIGURATION & PERSONA ---
st.set_page_config(page_title="MyTeacher | AI Kannada Tutor", layout="wide", initial_sidebar_state="expanded")

def apply_styles():
    st.markdown("""
        <style>
        .main { background-color: #FDFCFB; }
        .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
        .vocab-card { 
            background-color: #FFF9C4; 
            padding: 15px; 
            border-radius: 10px; 
            border-left: 5px solid #FBC02D;
            margin-bottom: 10px;
        }
        .teacher-prompt {
            font-style: italic;
            color: #2E7D32;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def process_lesson(input_data):
    # This simulates the "Thinking" phase where Alar.ink and Gemini work together
    # In production, this would call the APIs.
    lesson_content = {
        "title": "Lesson 1: Dr. Rajendra Prasad",
        "sections": [
            {
                "kannada": "ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು.",
                "explanation": "Dr. Rajendra Prasad was India's first President. He was famous because he was very simple and a very good human being.",
                "context": "Think of a superhero who doesn't wear a cape and is kind to everyone. That is 'Sajjanike'.",
                "vocab": [
                    {"word": "ಸರಳತೆ (Saralate)", "meaning": "Simplicity", "usage": "Living without showing off."},
                    {"word": "ಸಜ್ಜನಿಕೆ (Sajjanike)", "meaning": "Gentlemanliness", "usage": "Being noble and kind."}
                ]
            }
        ]
    }
    return lesson_content

# --- UI LAYOUT ---
def main():
    apply_styles()
    
    with st.sidebar:
        st.title("👨‍🏫 MyTeacher")
        st.info("Target Audience: 10-16 Years\nDialect: Bengaluru School Standard")
        language = st.selectbox("Explain in:", ["English", "Hindi"])
        st.divider()
        st.write("### 📒 Saved Word Bank")
        st.caption("Words will appear here as you learn.")

    st.title("Welcome to your Kannada Lesson")
    
    # Input Area
    input_col1, input_col2 = st.columns([2, 1])
    with input_col1:
        doc_input = st.file_uploader("Upload Lesson Screenshot or PDF", type=["png", "jpg", "pdf"])
    with input_col2:
        url_input = st.text_input("Or Paste Lesson URL")

    if st.button("Start Learning with MyTeacher"):
        if doc_input or url_input:
            lesson = process_lesson(None)
            
            st.divider()
            st.header(lesson["title"])
            
            # Classroom View
            col_left, col_right = st.columns([3, 2])
            
            with col_left:
                for idx, section in enumerate(lesson["sections"]):
                    st.subheader(f"Paragraph {idx+1}")
                    st.success(section["kannada"])
                    
                    with st.chat_message("assistant", avatar="👨‍🏫"):
                        st.write(f"**Teacher:** {section['explanation']}")
                        st.write(f"💡 **Context:** {section['context']}")
                        
                        # Audio Placeholder (In prod: ElevenLabs API)
                        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
                        st.caption("🔊 Paced at 0.8x with pedagogical pauses.")

            with col_right:
                st.write("### 🔍 Word Meanings (via Alar.ink)")
                for item in section["vocab"]:
                    st.markdown(f"""
                        <div class="vocab-card">
                            <b>{item['word']}</b><br>
                            <i>{item['meaning']}</i><br>
                            <small>{item['usage']}</small>
                        </div>
                    """, unsafe_allow_html=True)

            # Holistic Review
            st.divider()
            st.write("### 🤔 Let's Reflect")
            st.markdown('<p class="teacher-prompt">Dr. Prasad was the President but lived like a common man. Can you think of a time when you were simple even though you won a prize?</p>', unsafe_allow_html=True)
            
            review_input = st.text_area("Your thoughts (English/Hindi/Kannada):")
            if st.button("Submit Reflection"):
                st.balloons()
                st.success("Great reflection! You are connecting with the lesson's heart.")

if __name__ == "__main__":
    main()
