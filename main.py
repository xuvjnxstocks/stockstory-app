import streamlit as st
import openai

# Initialize OpenAI client with your secret key
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit page setup
st.set_page_config(page_title="Stock Story", page_icon="📈")
st.title("📘 AI Stock Story Summarizer")

# Ticker input
ticker = st.text_input("Enter a stock ticker (e.g. AAPL):")

# When user submits a ticker
if ticker:
    st.write(f"🔍 Generating company story for: {ticker.upper()}")

    # Prompt for GPT
    prompt = f"""
    You are a stock market educator. Explain what {ticker.upper()} does, summarize its recent financial performance, and any known news or risks, in simple language for a student or new investor.
    """

    # New OpenAI v1 API call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract and show response
    story = response.choices[0].message.content
    st.subheader("🧠 Company Summary")
    st.write(story)
