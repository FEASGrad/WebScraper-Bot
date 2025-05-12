import streamlit as st
import asyncio
from scraper import scrape_streaming

st.title("📘 Faculty Research Scraper")

if st.button("Start Scraping"):
    status = st.empty()
    progress = []

    async def run_scraper():
        async for msg in scrape_streaming():
            progress.append(msg)
            status.text("\n".join(progress[-10:]))

    asyncio.run(run_scraper())

    with open("Faculty_Academic_Interests.xlsx", "rb") as f:
        st.download_button("📥 Download Excel", f, "Faculty_Academic_Interests.xlsx")
