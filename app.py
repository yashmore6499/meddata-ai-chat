import streamlit as st
import pandas as pd
import google.generativeai as genai
from helper import load_data, df_to_text

# ✅ Set page config first
st.set_page_config(page_title="🧠 MedData AI Chat", layout="centered")

# 🎨 Custom CSS for pastel green theme with full animated background and floating medicine icons
custom_css = """
<style>
html, body, [data-testid="stAppViewContainer"]  {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow-y: auto;
    background: radial-gradient(circle, #ffffff66 0%, #d0f5d6 100%) !important;
    background-size: 400% 400%;
    animation: floatAnim 20s ease-in-out infinite;
    position: relative;
}

@keyframes floatAnim {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating medicine icon overlay */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('https://www.freepik.com/free-psd/blue-white-pills-levitating-midair-medicine-healthcare-wellness-treatment_410552449.htm#fromView=keyword&page=1&position=2&uuid=d87436f8-e39d-4207-89eb-aae95f263701&query=Medicine+Png');
    background-repeat: repeat;
    background-size: 50px;
    opacity: 0.05;
    animation: medicineFloat 100s linear infinite;
    z-index: -1;
    pointer-events: none;
}

@keyframes medicineFloat {
    0% { background-position: 0 0; }
    100% { background-position: 0 1000px; }
}

h1, h2, h3, h4, label, .stTextInput label, .stFileUploader label, .stCaption, .stMarkdown {
    color: #003300 !important;
}
.stButton button {
    background-color: #00cc88 !important;
    color: white !important;
    border-radius: 8px;
    font-weight: bold;
}
/* Glowing output style */
.glow-output {
    color: #003300;
    text-shadow: 0 0 5px white, 0 0 10px #fff, 0 0 15px #00ff88;
    font-size: 18px;
    font-weight: 600;
    padding: 10px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.2);
    margin-top: 10px;
    overflow-wrap: break-word;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 🧠 App Title
st.title("🧠 Gemini Medical Data Assistant")
st.caption("Upload your medical dataset and ask professional questions. Gemini AI will respond intelligently.")

# 🔑 Gemini API Key input
api_key = st.text_input("🔑 Enter your Gemini API Key:", type="password")
if not api_key:
    st.warning("⚠️ Please enter your Gemini API key to continue.")
    st.stop()

# 🔧 Gemini Configuration
genai.configure(api_key=api_key)

# 📁 File Upload
uploaded_file = st.file_uploader("📁 Upload Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    # 💬 Ask a question
    user_query = st.text_input("💬 Ask a professional data question:")

    if user_query:
        with st.spinner("🔍 Gemini is analyzing your dataset..."):
            try:
                preview_text = df_to_text(df, max_rows=10)
                prompt = f"""
You are a professional medical data analyst.
Here is a preview of the uploaded dataset:

{preview_text}

Now respond professionally and insightfully to this question:
{user_query}
"""
                try:
                    model = genai.GenerativeModel("models/gemini-2.5-pro")
                    response = model.generate_content(prompt)
                except Exception as e:
                    st.warning("⚠️ Gemini 2.5 Pro quota exceeded. Falling back to 1.5 Flash.")
                    model = genai.GenerativeModel("models/gemini-1.5-flash")
                    response = model.generate_content(prompt)

                st.markdown("### ✅ Gemini’s Answer:")
                st.markdown(f"<div class='glow-output'>{response.text.strip()}</div>", unsafe_allow_html=True)

                # Auto scroll to bottom
                st.markdown("""
                    <script>
                        window.scrollTo(0, document.body.scrollHeight);
                    </script>
                """, unsafe_allow_html=True)

            except Exception as e:
                if "quota" in str(e).lower():
                    st.error("🚫 Quota limit hit. Please wait a minute before retrying.")
                    if st.button("🔄 Retry Now"):
                        st.experimental_rerun()
                else:
                    st.error(f"❌ Gemini API Error: {e}")
