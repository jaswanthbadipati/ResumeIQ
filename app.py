import streamlit as st
import pdfplumber
from groq import Groq
import json
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="🎯",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .score-box {
        text-align: center;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .score-number {
        font-size: 4rem;
        font-weight: 700;
        line-height: 1;
    }
    .score-label { font-size: 1rem; margin-top: 0.5rem; }
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
    }
    .tag-missing  { background: #FCEBEB; color: #A32D2D; }
    .tag-present  { background: #EAF3DE; color: #3B6D11; }
    .suggestion-card {
        border-left: 3px solid #378ADD;
        padding: 0.75rem 1rem;
        background: #f8fafc;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Groq setup ───────────────────────────────────────────────────────────────
def get_model():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("Add your GROQ_API_KEY to Streamlit secrets (Settings → Secrets).")
        st.stop()
    return Groq(api_key=api_key)


# ── PDF text extraction ───────────────────────────────────────────────────────
def extract_pdf_text(uploaded_file) -> str:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


# ── Groq analysis ────────────────────────────────────────────────────────────
def analyze_resume(client, resume_text: str, jd_text: str) -> dict:
    prompt = f"""
You are an expert ATS (Applicant Tracking System) resume analyst and career coach.

Analyze the resume against the job description and return a JSON object ONLY (no markdown, no explanation outside JSON).

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{jd_text}
\"\"\"

Return this exact JSON structure:
{{
  "ats_score": <integer 0-100>,
  "score_verdict": "<one of: Poor | Fair | Good | Excellent>",
  "score_reason": "<2-sentence explanation of the score>",
  "keyword_analysis": {{
    "present": ["keyword1", "keyword2"],
    "missing": ["keyword1", "keyword2"]
  }},
  "section_feedback": [
    {{
      "section": "<Section name e.g. Summary, Experience, Skills, Education>",
      "issue": "<what is wrong or missing>",
      "suggestion": "<specific actionable fix>"
    }}
  ],
  "quick_wins": [
    "<Short 1-line tip that instantly improves ATS score>"
  ],
  "rewritten_summary": "<An improved professional summary optimized for this JD>"
}}

Rules:
- ats_score: strictly based on keyword match, formatting, relevance, quantifiable achievements
- missing keywords: only important ones from JD that are absent in resume
- section_feedback: max 5 sections, only real issues
- quick_wins: exactly 4 tips
- rewritten_summary: keep it under 4 lines, ATS-optimized
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content.strip()
    return json.loads(raw)


# ── Score color helper ────────────────────────────────────────────────────────
def score_color(score: int):
    if score >= 80: return "#3B6D11", "#EAF3DE"
    if score >= 60: return "#185FA5", "#E6F1FB"
    if score >= 40: return "#BA7517", "#FAEEDA"
    return "#A32D2D", "#FCEBEB"


# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🎯 ATS Resume Analyzer")
st.caption("Upload your resume + paste the job description → get your ATS score and exact fixes to land the interview.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Your Resume")
    uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} uploaded")

with col2:
    st.subheader("💼 Job Description")
    jd_text = st.text_area(
        "Paste the full job description here",
        height=220,
        placeholder="Paste the complete job description including required skills, responsibilities, and qualifications...",
        label_visibility="collapsed",
    )

st.divider()

analyze_btn = st.button("🔍 Analyze My Resume", type="primary", use_container_width=True)

if analyze_btn:
    if not uploaded_file:
        st.warning("Please upload your resume PDF.")
        st.stop()
    if not jd_text.strip():
        st.warning("Please paste the job description.")
        st.stop()

    with st.spinner("Extracting resume text..."):
        resume_text = extract_pdf_text(uploaded_file)

    if not resume_text:
        st.error("Could not extract text from the PDF. Make sure it's not a scanned image PDF.")
        st.stop()

    model = get_model()

    with st.spinner("Analyzing with Llama 3.3 70B via Groq — this takes ~10 seconds..."):
        try:
            result = analyze_resume(model, resume_text, jd_text)
        except json.JSONDecodeError:
            st.error("Model returned an unexpected response. Please try again.")
            st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # ── Results ───────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Analysis Results")

    # Score
    score = result.get("ats_score", 0)
    verdict = result.get("score_verdict", "")
    reason = result.get("score_reason", "")
    text_color, bg_color = score_color(score)

    sc1, sc2, sc3 = st.columns([1, 1, 2])
    with sc1:
        st.markdown(f"""
        <div class="score-box" style="background:{bg_color};">
            <div class="score-number" style="color:{text_color};">{score}</div>
            <div class="score-label" style="color:{text_color}; font-weight:600;">/ 100 — {verdict}</div>
        </div>
        """, unsafe_allow_html=True)
    with sc2:
        st.metric("Keywords Present", len(result.get("keyword_analysis", {}).get("present", [])))
        st.metric("Keywords Missing", len(result.get("keyword_analysis", {}).get("missing", [])))
    with sc3:
        st.info(f"**Why this score?**\n\n{reason}")

    st.divider()

    # Keyword Analysis
    kw = result.get("keyword_analysis", {})
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### ✅ Keywords Found")
        present = kw.get("present", [])
        if present:
            tags = " ".join([f'<span class="tag tag-present">{k}</span>' for k in present])
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.caption("No matching keywords found.")

    with col_b:
        st.markdown("#### ❌ Missing Keywords")
        missing = kw.get("missing", [])
        if missing:
            tags = " ".join([f'<span class="tag tag-missing">{k}</span>' for k in missing])
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.caption("No critical keywords missing — great!")

    st.divider()

    # Section Feedback
    st.markdown("#### 🛠 Section-by-Section Fixes")
    for item in result.get("section_feedback", []):
        with st.expander(f"**{item.get('section', 'Section')}** — {item.get('issue', '')[:60]}..."):
            st.markdown(f"**Issue:** {item.get('issue', '')}")
            st.markdown(f"**Fix:** {item.get('suggestion', '')}")

    st.divider()

    # Quick Wins
    st.markdown("#### ⚡ Quick Wins — Do These First")
    qw = result.get("quick_wins", [])
    for i, tip in enumerate(qw, 1):
        st.info(f"**{i}.** {tip}")

    st.divider()

    # Rewritten Summary
    st.markdown("#### ✍️ AI-Optimized Professional Summary")
    st.caption("Replace your current summary with this ATS-optimized version:")
    st.code(result.get("rewritten_summary", ""), language=None)

    st.divider()
    st.success("✅ Analysis complete! Apply the fixes above and re-analyze to push your score above 80.")
    st.caption("Tip: Missing keywords should be naturally added to your Skills, Summary, or Experience bullets.")