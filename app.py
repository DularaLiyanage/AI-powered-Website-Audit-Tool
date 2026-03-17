import streamlit as st
from analyzer import analyze_page
from ai_insights import generate_ai_insights
import re

st.set_page_config(page_title="AI Website Audit Tool")

st.title("🔍 AI Website Audit Tool")

url = st.text_input("Enter Website URL")

if st.button("Analyze"):

    if not url:
        st.error("Please enter a valid URL")
    else:
        with st.spinner("Analyzing website..."):

            try:
                metrics, content = analyze_page(url)
                ai_output = generate_ai_insights(url, metrics, content)

                st.subheader("📊 Factual Metrics")
                st.json(metrics)

                st.subheader("🤖 AI Insights & Recommendations")
                st.write(ai_output)

            except Exception as e:
                st.error(f"Error: {e}")