import streamlit as st
from analyzer import analyze_page
from ai_insights import generate_ai_insights
import re

st.set_page_config(page_title="AI Website Audit Tool", layout="wide")

# ---------------------------
# HEADER
# ---------------------------
st.title("🔍 AI Website Audit Tool")
st.markdown("Analyze any webpage for SEO, UX, and conversion insights.")

st.markdown("---")

# ---------------------------
# INPUT
# ---------------------------
url = st.text_input("Enter Website URL")

# ---------------------------
# ANALYZE BUTTON
# ---------------------------
if st.button("Analyze"):

    if not url:
        st.error("Please enter a valid URL")
    else:
        with st.spinner("Analyzing website..."):

            try:
                metrics, content = analyze_page(url)
                ai_output = generate_ai_insights(url, metrics, content)

                st.success("✅ Analysis Complete")

                st.markdown("---")

                # ---------------------------
                # SCORE SECTION
                # ---------------------------
                score_match = re.search(r"Score:\s*(\d+)/100", ai_output)

                if score_match:
                    score = int(score_match.group(1))

                    if score >= 75:
                        st.success(f"📊 Overall Score: {score}/100")
                    elif score >= 50:
                        st.warning(f"📊 Overall Score: {score}/100")
                    else:
                        st.error(f"📊 Overall Score: {score}/100")

                # ---------------------------
                # METRICS SECTION (IMPROVED)
                # ---------------------------
                st.subheader("📊 Factual Metrics")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Word Count", metrics["word_count"])
                col2.metric("CTAs", metrics["cta_count"])
                col3.metric("Images", metrics["images"]["total"])
                col4.metric(
                    "Missing Alt %",
                    f"{metrics['images']['missing_alt_percent']}%"
                )

                st.markdown("### Detailed Metrics")
                st.json(metrics)

                st.markdown("---")

                # ---------------------------
                # AI OUTPUT
                # ---------------------------
                st.subheader("🤖 AI Insights & Recommendations")
                st.markdown(ai_output)

            except Exception as e:
                st.error(f"Error: {e}")