import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCEzcqYkqH3H32Y4S2PdzgAQ1Q_4sgR3t4 ")
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("🤖 Professor Recommender Bot")

uploaded_file = st.file_uploader("Upload Faculty Excel File (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Prepare professor context once
    prof_context = ""
    for _, row in df.iterrows():
        prof_context += f"Name: {row['Name']}\nLink: {row['Profile Link']}\nResearch: {row['All Text']}\n\n"

    # Initialize state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # Display chat history
    for user_q, bot_r in st.session_state.chat_history:
        st.markdown(f"**You:** {user_q}")
        st.markdown(f"**Bot:** {bot_r}")

    # Chat input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask a research-related question:", value="")
        submitted = st.form_submit_button("Ask")

    # Handle submission
    if submitted and user_input:
        # Save user input to session
        st.session_state.user_input = user_input

        # Build full prompt context
        chat_prompt = f"""
You are an expert assistant helping students find professors based on their research interests.
You will be given a list of professors and their research areas. Recommend 6 professors whose research best matches the query.
Include profile links and 5-sentence summaries of their work. Only aswer with the names of the professors and their links and research areas in paragraph form.

Professor Data:
{prof_context}

Conversation so far:
"""
        for u, b in st.session_state.chat_history:
            chat_prompt += f"User: {u}\nBot: {b}\n"
        chat_prompt += f"User: {user_input}\nBot:"

        with st.spinner("🤖 Thinking..."):
            try:
                response = model.generate_content(chat_prompt)
                reply = response.text.strip()
            except Exception as e:
                reply = f"❌ Error: {e}"

        # Append to history and clear input
        st.session_state.chat_history.append((user_input, reply))
        st.session_state.user_input = ""

        # Force immediate refresh to show reply and input again
        st.rerun()
