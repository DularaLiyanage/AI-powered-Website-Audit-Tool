import streamlit as st
from analyzer import analyze_page
from ai_insights import generate_ai_insights
import re

st.set_page_config(page_title="AI Website Audit Tool", layout="wide")

# HEADER
st.title("AI Website Audit Tool")
st.markdown("Analyze any webpage for SEO, UX, and conversion insights.")

st.markdown("---")

# INPUT
url = st.text_input("Enter Website URL")

# ANALYZE BUTTON
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

                # SCORE SECTION
                score_match = re.search(r"(?i)score\b\W*(\d+)(?:/100)?", ai_output)

                if not score_match: 
                    st.info("📊 Score not available")

                if score_match: 
                    score = int(score_match.group(1))

                    if score >= 75: 
                        st.success(f"📊 Overall Score: {score}/100")
                    elif score >= 50: 
                        st.warning(f"📊 Overall Score: {score}/100") 
                    else: 
                        st.error(f"📊 Overall Score: {score}/100")

                st.markdown("---")

                # METRICS SECTION
                h1_count = len(metrics["headings"]["h1"])
                h2_count = len(metrics["headings"]["h2"])
                h3_count = len(metrics["headings"]["h3"])
                
                st.subheader("📊 Factual Metrics")

                with st.container():
                    st.markdown("**Content & Media**")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Word Count", metrics["word_count"])
                    col2.metric("Images", metrics["images"]["total"])
                    col3.metric("Missing Alt %", f"{metrics['images']['missing_alt_percent']}%")
                
                with st.container():
                    st.markdown("**Heading Structure**")
                    col4, col5, col6 = st.columns(3)
                    col4.metric("H1 Tags", h1_count)
                    col5.metric("H2 Tags", h2_count)
                    col6.metric("H3 Tags", h3_count)

                with st.container():
                    st.markdown("**Links & Actions**")
                    col7, col8, col9 = st.columns(3)
                    col7.metric("Internal Links", metrics["links"]["internal"])
                    col8.metric("External Links", metrics["links"]["external"])
                    col9.metric("CTAs", metrics["cta_count"])
                
                st.markdown("### Detailed Metrics")
                st.json({
                    **metrics,
                    "headings": {
                        "h1_count": h1_count,
                        "h2_count": h2_count,
                        "h3_count": h3_count,
                        "h1_text": metrics["headings"]["h1"],
                        "h2_text": metrics["headings"]["h2"],
                        "h3_text": metrics["headings"]["h3"],
                    }
                })

                st.markdown("---")

                # AI OUTPUT
                st.subheader("AI Insights & Recommendations")
                formatted_output = ai_output.replace("\n", "\n\n")

                st.markdown(formatted_output)

            except Exception as e:
                st.error(f"Error: {e}")