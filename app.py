import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCEzcqYkqH3H32Y4S2PdzgAQ1Q_4sgR3t4 ")
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("Find your FEAS Grad Research Supervisors")

# Load the existing spreadsheet from the same directory (replace 'Faculty_Academic_Interests.xlsx' with your file)
EXCEL_FILE = "Faculty_Academic_Interests.xlsx"
df = pd.read_excel(EXCEL_FILE)

# Prepare professor context once
prof_context = ""
for _, row in df.iterrows():
    prof_context += f"Name: {row['Name']}\nLink: {row['Profile Link']}\nResearch: {row['All Text']}\n\n"

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Display chat history
for user_q, bot_r in st.session_state.chat_history:
    st.markdown(f"**You:** {user_q}")
    st.markdown(f"**Bot:** {bot_r}")

# Define a callback to handle input submission and update state
def submit():
    user_input = st.session_state.input_text.strip()
    if not user_input:
        return  # ignore empty input
    
    # Build the prompt
    chat_prompt = f"""
You are an expert assistant helping students find professors based on their research interests.
You will be given a list of professors and their research areas. Recommend as many professors whose research best matches the query.
Include profile links and 5-sentence summaries of their work. Only answer with paragraph form.

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

    # Append to chat history
    st.session_state.chat_history.append((user_input, reply))

    # Clear input text after submission
    st.session_state.input_text = ""

# Use a text_input linked to session state with a callback for form submission
with st.form(key="chat_form", clear_on_submit=False):
    user_input = st.text_input("Ask a research-related question:", key="input_text")
    submitted = st.form_submit_button("Ask", on_click=submit)

