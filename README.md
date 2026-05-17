# 🎯 ResumeIQ — AI-Powered ATS Resume Analyzer

**Stop getting filtered out before a human even reads your resume.**

ResumeIQ analyzes your resume against any job description, gives you an ATS score, and tells you exactly what to fix — keyword gaps, weak sections, and a rewritten summary — all in under 15 seconds.

---

## 📸 Features

| | Feature | What it does |
|---|---|---|
| 📊 | **ATS Score** | 0–100 score with verdict: Poor / Fair / Good / Excellent |
| 🔑 | **Keyword Analysis** | Shows which JD keywords are present ✅ and which are missing ❌ |
| 🛠️ | **Section Feedback** | Per-section issues (Summary, Skills, Experience) with specific fixes |
| ⚡ | **Quick Wins** | 4 highest-impact changes to make right now |
| ✍️ | **AI Summary Rewrite** | Drops an ATS-optimized professional summary tailored to the JD |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| App framework | Streamlit |
| AI model | Llama 3.3 70B via Groq API |
| PDF parsing | pdfplumber |
| Deployment | Streamlit Community Cloud |
| **Total cost** | **₹0 / $0** |

---

## ⚙️ Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/resumeiq.git
cd resumeiq
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create the file `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_your_key_here"
```

Get a free API key at → [console.groq.com](https://console.groq.com) — no billing required, 14,400 requests/day free.

### 4. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub
3. Click **Create app** → select your repo → set main file as `app.py`
4. Go to **Advanced settings → Secrets** and add:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
5. Click **Deploy** — live URL ready in ~2 minutes

Your app will be live at:
```
https://yourusername-resumeiq-app-xxxxxx.streamlit.app
```

---

## 📁 Project Structure

```
resumeiq/
├── app.py                  # Entire app — frontend + AI logic
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API keys (never commit this)
└── README.md
```

---

## 🔒 Privacy

- Resumes are processed **in memory only** — nothing is stored or saved
- No database, no user accounts, no data retention
- Each analysis is completely stateless

---

## 🧠 How the ATS Score is Calculated

Llama 3.3 70B scores your resume based on:

- **Keyword match** — how many required JD keywords appear in your resume
- **Relevance** — does your experience align with the role responsibilities
- **Quantifiable achievements** — numbers, percentages, and impact metrics
- **Section completeness** — Summary, Skills, Experience, Education all present
- **Formatting signals** — clean sections and standard headings ATS can parse

> A score above **80** significantly increases your chances of passing ATS filters.

---

## 📦 Dependencies

```
streamlit>=1.35.0
pdfplumber>=0.10.3
groq>=0.9.0
```

---

## 🗺️ Roadmap

- [ ] DOCX resume upload support
- [ ] Score history across multiple analyses
- [ ] Side-by-side before/after view
- [ ] Export optimized suggestions as PDF
- [ ] Auto-fill JD from a LinkedIn job URL

---

## 👨‍💻 About

Built by **Jaswanth Badipati**
B.Tech AI & Data Science — VR Siddhartha Engineering College, Andhra Pradesh
TOMAN Dev Group · Google Developer Group Solution Challenge

---

## 📄 License

MIT — free to use, fork, and build on.
