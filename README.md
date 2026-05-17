# 🎯 ResumeIQ — AI-Powered ATS Resume Analyzer

> Upload your resume. Paste the job description. Get your ATS score and exact fixes to land the interview.



## ✨ What It Does

**ResumeIQ** analyzes your resume against any job description using Google Gemini 1.5 Flash and tells you exactly why you're getting filtered out by ATS systems — and how to fix it.

| Feature | Description |
|---|---|
| 📊 ATS Score | 0–100 score with verdict (Poor / Fair / Good / Excellent) |
| 🔑 Keyword Analysis | Green = found, Red = missing from JD |
| 🛠 Section Feedback | Per-section issues with specific fixes |
| ⚡ Quick Wins | 4 highest-impact changes to make right now |
| ✍️ AI Summary Rewrite | Optimized professional summary for the JD |

---

## 🛠 Tech Stack

| Layer | Tool | Cost |
|---|---|---|
| Frontend + Backend | Streamlit | Free |
| AI Model | Gemini 1.5 Flash | Free (15 req/min) |
| PDF Parsing | pdfplumber | Free |
| Deployment | Streamlit Community Cloud | Free |

**Total cost: ₹0**

---

## ⚙️ Setup — Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/resumeiq.git
cd resumeiq
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create a file at `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Get a free API key at → [aistudio.google.com](https://aistudio.google.com) (no billing required)

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy Free on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo and set `app.py` as the main file
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **Deploy** — your app is live in ~2 minutes with a public URL

---

## 📁 Project Structure

```
resumeiq/
├── app.py               # Main Streamlit app (all-in-one)
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── secrets.toml     # API key (never commit this)
└── README.md
```

---

## 🔒 Privacy

- Resumes are processed **in memory only** — nothing is stored or logged
- No database, no user accounts, no data retention
- Each session is completely stateless

---

## 🧠 How the ATS Score Works

The score is calculated by Gemini based on:

- **Keyword match** — how many JD keywords appear in your resume
- **Relevance** — does your experience align with the role
- **Quantifiable achievements** — numbers, percentages, impact metrics
- **Formatting signals** — clean sections, standard headings, no tables/columns that ATS can't parse
- **Section completeness** — Summary, Skills, Experience, Education all present

A score above **80** significantly increases your chances of passing ATS filters.

---

## 📦 Dependencies

```
streamlit>=1.35.0
pdfplumber>=0.10.3
google-generativeai>=0.7.0
```

---

## 🤝 Contributing

Pull requests welcome! Ideas for improvement:

- [ ] Support DOCX resume uploads
- [ ] Side-by-side before/after resume view
- [ ] Export optimized resume suggestions as PDF
- [ ] History of past analyses (with Supabase free tier)
- [ ] LinkedIn job scraper to auto-fill JD

---

## 👨‍💻 Built By

**Jaswanth Badipati** — B.Tech AI & Data Science, VR Siddhartha Engineering College  
Part of TOMAN Dev Group | Google Developer Group Solution Challenge participant

---

## 📄 License

MIT License — free to use, modify, and distribute.
