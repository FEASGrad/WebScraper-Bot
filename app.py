import streamlit as st
import pandas as pd
import google.generativeai as genai

# Setup Gemini API
genai.configure(api_key="AIzaSyA-fV7I7YcLr5KiYHzK4Ug84P0eEC9m79E")
model = genai.GenerativeModel("gemini-pro")

st.title("🤖 Professor Recommender Bot")

uploaded_file = st.file_uploader("Upload Faculty Excel File (.xlsx)", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    user_query = st.text_input("Ask a research-related question:")
    
    if user_query:
        context = ""
        for i, row in df.iterrows():
            context += f"Name: {row['Name']}\nLink: {row['Profile Link']}\nResearch: {row['All Text']}\n\n"

        prompt = f"""
        Based on the following professor data, recommend those whose research matches this query: "{user_query}".
        Return names and profile links. Data:\n\n{context}
        """

        response = model.generate_content(prompt)
        st.markdown(response.text)
