# AI-Powered Website Audit Tool

This tool is a lightweight, AI-driven website audit application. It takes a single URL, extracts factual layout metrics (word count, headings, CTAs, internal/external links, and images), and leverages OpenAI to generate an actionable audit covering SEO, UX, and conversion insights.

## Live Application

Deployed on Streamlit Community Cloud: [https://ai-powered-website-audit-tool.streamlit.app/](https://ai-powered-website-audit-tool.streamlit.app/)

## Deliverables & Links

1. **GitHub Repository**: ([The current directory where this system sits](https://github.com/DularaLiyanage/AI-powered-Website-Audit-Tool))
2. **Local Web App Instructions**: See [Setup & Run Instructions](#setup--run-instructions) below.
3. **Prompt Logs**: Found in the `prompt_logs/` directory after a successful analysis.

---

## Architecture Overview

The tool is divided into three key areas, designed with a clean separation of concerns:

1. **Extraction Layer (`analyzer.py`)**: Uses `requests` and `BeautifulSoup` to scrape the provided URL. It parses out specific HTML elements to generate factual metrics (word count, CTA detection, image alt text analysis) and returns the core text.
2. **AI Analysis Layer (`ai_insights.py`)**: Responsible for constructing the context window for the AI. It relies heavily on strict prompt engineering to give the AI context. It sends the factual metrics alongside the text content and ensures a predictable markdown schema is returned containing actionable insights.
3. **Frontend Presentation (`app.py`)**: Built on **Streamlit**, this layer ties the application together, handling user input, displaying factual metrics clearly alongside the structured AI evaluations, and gracefully parsing the AI layer's output format.

---

## AI Design Decisions

1. **Metrics as the Primary Source of Truth**: The AI is instructed to base its insights primarily on the numeric data provided from BeautifulSoup (e.g., word count, tags counts, missing alt tags), while using the parsed `<text>` only to supplement its reasoning. This grounds the AI in reality instead of letting it hallucinate layout elements.

2. **Strict Output Formatting Guidelines**: Enforced a predictable output structure by injecting a rigid `OUTPUT STRUCTURE` template into the system prompt. By heavily defining the expected markdown headers (e.g., `1. SEO STRUCTURE`, `6. PRIORITIZED RECOMMENDATIONS`, `7. OVERALL SCORE (0–100)`), this can parse out the exact scores programmatically via regex in the frontend while still allowing the LLM to write flowing contextual paragraphs.

3. **Structured Prompt Configuration**: The system prompt clearly delineates guidelines and rules. Giving the AI a persona ("senior SEO consultant") ensures the language is not generic but rather practical, actionable agency advice.

---

## Trade-offs

* **Heuristic CTA Detection**: Rather than spinning up a full headless browser to analyze CSS classes and visual placement, I detected `<button>`, `<input type="submit">`, and `<a>` elements containing common action text ("buy", "sign up"). This is lighter and faster, but misses visual buttons that don't stick to these heuristics.

* **Timeout Constraints**: The scraper operates with a 10s timeout on `requests`. Extremely slow sites or sites aggressively blocking non-browser agents may crash or return incomplete data.

* **Single-Page Constraint**: Metrics like "Internal Links" are pulled, but I don't follow them to gauge site-wide structure. The tool provides a micro-audit, not a macro-audit.

* **JavaScript Heavy Frameworks (React/Vue)**: Because the tool relies on raw HTML parsing via BeautifulSoup, URLs generating their DOM dynamically via client-side javascript will lack content for accurate analysis.

---

## What Would You Improve With More Time

1. **Playwright Integration**: Render JS-heavy pages fully before scraping, 
   enabling accurate analysis of React/Vue/Angular SPAs.

2. **Vision API**: Screenshot the rendered page and pass it to GPT-4o vision 
   for real visual hierarchy, contrast, and layout analysis.

3. **Confidence Scoring**: Add a secondary LLM pass to rate each 
   recommendation by estimated impact vs implementation effort.

4. **Structured JSON Output**: Use OpenAI's structured outputs / response 
   format to enforce a strict JSON schema rather than regex parsing.

5. **Site-wide Crawl**: Follow internal links up to a configurable depth 
   for macro-level audits using the sitemap.

---

## Setup & Run Instructions

This tool requires Python 3.8+.

1. **Clone the repository**
```bash
   git clone https://github.com/DularaLiyanage/AI-powered-Website-Audit-Tool
   cd AI-powered-Website-Audit-Tool
```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables:**
   Ensure you have a `.env` file in the root directory containing your OpenAI Key:
   ```
   OPENAI_API_KEY=your_key_here
   ```
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
4. **Usage:**
   - In your browser, enter a URL.
   - Click "Analyze" and wait (~10-20 seconds).
   - Review the Factual Metrics vs Structured AI Output. 
   - Check `prompt_logs` for the full prompt traces

## Deployment to Streamlit Cloud

This tool is built with Streamlit and is currently hosted on Streamlit Community Cloud : [https://ai-powered-website-audit-tool.streamlit.app/](https://ai-powered-website-audit-tool.streamlit.app/)

## Prompt Log Structure

Each audit saves a JSON file to `prompt_logs/` containing:
```json
{
  "url": "...",
  "timestamp": "...",
  "system_prompt": "...",
  "user_prompt": "...",
  "input_metrics": { ... },
  "raw_output": "..."
}
```
## Final Notes

This project demonstrates:
-AI-native thinking (beyond simple API usage)
-Grounding AI in structured data
-Clean modular architecture
-Real-world applicability for web agencies