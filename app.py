import streamlit as st
import requests
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="MyTeacher Pro | Contextual Mastery", layout="wide", page_icon="👨‍🏫")

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Noto+Sans+Kannada:wght@400;700&display=swap');
        
        .main { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
        
        /* Premium Lesson Card */
        .lesson-card {
            background: white; padding: 40px; border-radius: 20px;
            border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            font-family: 'Noto Sans Kannada', sans-serif; font-size: 1.6rem;
            line-height: 2.2; color: #1E293B;
        }

        /* Contextual Word Card - Blue Accent */
        .word-card {
            background: #FFFFFF; border-radius: 12px; padding: 20px;
            border: 1px solid #E2E8F0; margin-bottom: 20px;
            border-left: 6px solid #4338CA;
            transition: transform 0.2s;
        }
        .word-card:hover { transform: scale(1.01); }
        .word-title { color: #4338CA; font-weight: 700; font-size: 1.2rem; margin-bottom: 5px; }
        .meaning-section { font-size: 1rem; color: #334155; margin-bottom: 10px; }
        
        /* Make Sentence Box */
        .usage-box {
            background: #F1F5F9; padding: 12px; border-radius: 8px; border-left: 3px solid #64748B;
            margin-top: 10px;
        }
        .usage-label { font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 4px; }
        .kannada-sentence { font-family: 'Noto Sans Kannada', sans-serif; color: #0F172A; font-weight: 600; }
        .translation-text { font-style: italic; color: #475569; font-size: 0.9rem; }
        </style>
    """, unsafe_allow_html=True)

# --- LESSON DATA ---
PARAGRAPH_DATA = {
    "text": """ಭಾರತದ ಪ್ರಥಮ ರಾಷ್ಟ್ರಪತಿಗಳಾದ ಡಾ. ರಾಜೇಂದ್ರ ಪ್ರಸಾದ್ ಅವರು ಸರಳತೆ ಮತ್ತು ಸಜ್ಜನಿಕೆಗೆ ಹೆಸರಾದವರು. 
    ಅವರು ಸ್ವಾತಂತ್ರ್ಯ ಹೋರಾಟದಲ್ಲಿ ಸಕ್ರಿಯವಾಗಿ ಪಾಲ್ಗೊಂಡಿದ್ದರು ಮತ್ತು ಸಂವಿಧಾನ ರಚನಾ ಸಭೆಯ ಅಧ್ಯಕ್ಷರಾಗಿ ಸೇವೆ ಸಲ್ಲಿಸಿದರು.""",
    "words": [
        {
            "word": "ಸರಳತೆ (Saralate)",
            "meaning": "Simplicity / सादगी",
            "usage_kn": "ಗಾಂಧೀಜಿಯವರ ಸರಳತೆ ಎಲ್ಲರಿಗೂ ಮಾದರಿ.",
            "usage_en": "Gandhiji's simplicity is a model for everyone.",
            "usage_hi": "गांधीजी की सादगी सभी के लिए एक आदर्श है."
        },
        {
            "word": "ಸಜ್ಜನಿಕೆ (Sajjanike)",
            "meaning": "Gentleness / सज्जनता",
            "usage_kn": "ಅವರ ಸಜ್ಜನಿಕೆ ನಮ್ಮನ್ನು ಬೆರಗುಗೊಳಿಸಿತು.",
            "usage_en": "Their gentleness amazed us.",
            "usage_hi": "उनकी सज्जनता ने हमें चकित कर दिया."
        },
        {
            "word": "ಸ್ವಾತಂತ್ರ್ಯ (Svatantrya)",
            "meaning": "Independence / स्वतंत्रता",
            "usage_kn": "ಭಾರತವು 1947 ರಲ್ಲಿ ಸ್ವಾತಂತ್ರ್ಯ ಪಡೆಯಿತು.",
            "usage_en": "India gained independence in 1947.",
            "usage_hi": "भारत को 1947 में स्वतंत्रता मिली."
        },
        {
            "word": "ಹೋರಾಟ (Horata)",
            "meaning": "Struggle / संघर्ष",
            "usage_kn": "ಜೀವನವೇ ಒಂದು ದೊಡ್ಡ ಹೋರಾಟ.",
            "usage_en": "Life is a great struggle.",
            "usage_hi": "जीवन एक महान संघर्ष है."
        },
        {
            "word": "ಸಕ್ರಿಯ (Sakriya)",
            "meaning": "Active / सक्रिय",
            "usage_kn": "ಅವನು ಶಾಲೆಯ ಚಟುವಟಿಕೆಗಳಲ್ಲಿ ಸಕ್ರಿಯನಾಗಿದ್ದಾನೆ.",
            "usage_en": "He is active in school activities.",
            "usage_hi": "वह स्कूल की गतिविधियों में सक्रिय है."
        }
    ]
}

def main():
    load_css()
    
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 15px;'>
            <h1 style='color: #0F172A;'>Contextual Mastery</h1>
            <span style='background: #4338CA; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;'>V1.3</span>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Deep Vocabulary Enrichment: Learn the meaning, see the usage, and master the context.")

    # Main Layout
    col_content, col_dictionary = st.columns([1, 1], gap="large")

    with col_content:
        st.subheader("📖 Paragraph Study")
        st.markdown(f'<div class="lesson-card">{PARAGRAPH_DATA["text"]}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div style='background: #1E293B; padding: 25px; border-radius: 15px; color: white;'>", unsafe_allow_html=True)
            st.markdown("### ✍️ Sentence Builder")
            st.write("Pick a word from the Insights panel and try to write your own sentence:")
            st.text_input("My Kannada Sentence:", placeholder="Type here...")
            st.button("Validate Sentence")
            st.markdown("</div>", unsafe_allow_html=True)

    with col_dictionary:
        st.subheader("📒 Alar Insights & Usage")
        st.info("Study these 10 words carefully to understand their role in the paragraph.")
        
        for item in PARAGRAPH_DATA["words"]:
            st.markdown(f"""
                <div class="word-card">
                    <div class="word-title">{item['word']}</div>
                    <div class="meaning-section"><b>Meaning:</b> {item['meaning']}</div>
                    
                    <div class="usage-box">
                        <div class="usage-label">Kannada Usage (Make Sentence)</div>
                        <div class="kannada-sentence">{item['usage_kn']}</div>
                    </div>
                    
                    <div style='display: flex; gap: 20px; margin-top: 10px;'>
                        <div style='flex: 1;'>
                            <div class="usage-label">English Translation</div>
                            <div class="translation-text">{item['usage_en']}</div>
                        </div>
                        <div style='flex: 1;'>
                            <div class="usage-label">Hindi Translation</div>
                            <div class="translation-text">{item['usage_hi']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
