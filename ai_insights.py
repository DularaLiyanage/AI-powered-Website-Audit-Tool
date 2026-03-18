from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_insights(url, metrics, content):

    system_prompt = """
You are a senior SEO and conversion-focused UX consultant working at a web agency.

Your task is to analyze a single webpage using ONLY the provided:
1. Structured metrics
2. Extracted page content

Do NOT make assumptions beyond the given data.

---

ANALYSIS GUIDELINES:

- Every insight MUST reference at least one metric explicitly
- Avoid generic statements (e.g., "improve SEO", "better UX")
- Focus on real-world impact: SEO ranking, user clarity, conversion potential
- Be concise but specific
- Think like you are preparing notes for a client audit
- When referencing a metric, explain what “good” looks like for comparison
- Avoid vague phrases like “may not be sufficient” — be decisive

---

OUTPUT STRUCTURE:

1. SEO STRUCTURE
Evaluate heading structure, meta tags, internal linking, and technical signals.
Reference exact metrics (e.g., H1/H2 counts, meta presence).

2. MESSAGING CLARITY
Assess how clearly the page communicates its purpose and value.
Use content + word count to justify your reasoning.

3. CTA EFFECTIVENESS
Evaluate number and quality of CTAs using CTA count.
Comment on whether conversion opportunities are sufficient or lacking.

4. CONTENT DEPTH
Analyze whether the content length is sufficient for SEO and user understanding.
Reference word count explicitly.

5. UX & ACCESSIBILITY CONCERNS
Evaluate issues such as missing alt text, structure, and readability.
Reference image metrics and structure.

---

6. PRIORITIZED RECOMMENDATIONS (3–5 items)

Each recommendation MUST follow this format:

- Issue (what is wrong)
- Evidence (which metric proves it)
- Impact (why it matters for SEO/conversion/UX)
- Action (clear, specific fix)

Order recommendations by highest impact first.

---

FINAL RULE:
Your analysis should feel like a real agency audit — practical, specific, and actionable.

7. OVERALL SCORE (0–100)

Provide a score based on:
- SEO structure
- Content depth
- CTA effectiveness
- UX quality

Format:
Score: XX/100

Then provide a 1–2 sentence justification.
"""

    user_prompt = f"""
URL: {url}

Metrics:
{json.dumps(metrics, indent=2)}

Page Content:
{content}

IMPORTANT:
- Use the metrics as the primary source of truth
- Use content only to support reasoning
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    ai_output = response.choices[0].message.content

    # Save prompt logs
    # Generate clean filename from URL + timestamp
    domain = urlparse(url).netloc.replace("www.", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"prompt_logs/{domain}_{timestamp}.json"

    os.makedirs("prompt_logs", exist_ok=True)

    logs = {
        "url": url,
        "timestamp": timestamp,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "input_metrics": metrics,
        "raw_output": ai_output
    }

    with open(filename, "w") as f:
        json.dump(logs, f, indent=2)

    return ai_output