import streamlit as st
import openai

# ✅ This works with user-level keys
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit page setup
st.set_page_config(page_title="Stock Story", page_icon="📈")
st.title("📘 AI Stock Story Summarizer")

# Ticker input
ticker = st.text_input("Enter a stock ticker (e.g. AAPL):")

if ticker:
    st.write(f"🔍 Generating company story for: {ticker.upper()}")

    prompt = f"""
    You are a stock market educator. Explain what {ticker.upper()} does, summarize its recent financial performance, and any known news or risks, in simple language for a student or new investor.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    story = response['choices'][0]['message']['content']
    st.subheader("🧠 Company Summary")
    st.write(story)
