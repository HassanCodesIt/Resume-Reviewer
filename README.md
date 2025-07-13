<p align="center">
  <img src="https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/release-v1.0.0-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/coverage-95%25-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/contributors-welcome-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/downloads-1k%2B-blueviolet?style=for-the-badge"/>
</p>

# **Resume Reviewer**
**AI-Powered Resume & Job Fit Analyzer**

> *Snapshot:*
> ![App Dashboard Screenshot](docs/snapshot.png)  
> _Visual: Upload resume + JD, get instant analytics, feedback, and a pro report. (Replace with your own GIF/screenshot)_

---

## ✨ Description & Vision

**Resume Reviewer** is your no-nonsense, next-gen resume reviewer. Upload your resume and a job description, and get instant, actionable feedback, skill gap analysis, ATS optimization, and a match score—all in a slick dashboard.  
We’re building on the best of AI, NLP, and classic resume wisdom. This project fuses LLMs, semantic search, and industry-standard ATS checks, so you can level up your job hunt and keep it 100. No cap: this is the future of job matching, but with respect for what’s always worked.

---

## 🖥️ Tech Stack

**Frontend:**
- Bootstrap 5 (UI framework)
- Chart.js (visual analytics)
- Jinja2 (templating)
- Custom JavaScript (main.js)
- Custom CSS (styles.css)

**Backend:**
- Python 3.8+
- Flask (web framework)
- Flask-WTF (form handling, CSRF)
- Jinja2 (server-side rendering)
- python-dotenv (env management)

**AI & NLP:**
- Hugging Face Inference API (LLM feedback, e.g., Llama 3)
- Sentence Transformers (all-MiniLM-L6-v2 for embeddings)
- spaCy (en_core_web_sm for NLP/skills)
- scikit-learn (cosine similarity)

**PDF & File Handling:**
- pdfminer.six (PDF text extraction)
- pdfkit (PDF export)
- wkhtmltopdf (required for PDF export)

**Other:**
- Environment variables for secrets/API keys
- Session-based state (no persistent DB)
- Modular, extensible codebase

---

## 🗂️ Table of Contents

- [Installation](#installation)
- [Features](#usage--features)
- [Usage](#usage--features)
- [Architecture](#architecture--mermaid-diagram)
- [Mermaid Diagram](#architecture--mermaid-diagram)
- [Contributing](#contributing--community)
- [License](#license--support)

---

## ⚡ Installation

- **Prerequisites:** Python 3.8+, pip, [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) (for PDF export), Hugging Face account.
- **Clone & install:**
  ```bash
  git clone https://github.com/your-org/resume-insight-ai.git
  cd resume-insight-ai
  pip install -r requirements.txt
  python -m spacy download en_core_web_sm
  ```
- **Set up `.env`:**
  ```
  HF_TOKEN=your_huggingface_token
  SECRET_KEY=your_flask_secret
  ```
- **Run:**
  ```bash
  python run.py
  ```
  Visit [http://localhost:5000](http://localhost:5000)

---

## 🚀 Usage & Features

**How it works:**  
Upload or paste your resume and a job description (PDF or text). Click “Analyze.”  
Get a dashboard with:

- **Semantic Job Fit Score** — See how well you match (with a breakdown).
- **Skill Extraction & Gap Analysis** — Instantly see what you have and what you’re missing.
- **AI-Powered Feedback** — LLM-generated, actionable, and categorized suggestions.
- **ATS Optimization Report** — Checklist for passing automated screeners.
- **Visual Analytics** — Pie charts, gauges, word clouds.
- **Downloadable PDF Report** — Print-friendly, pro-style.

**Example:**
```text
Match Score: 82% (Strong Fit)
Missing Skills: AWS, CI/CD
AI Suggestion: “Add hands-on cloud experience and link to your GitHub.”
```
![Dashboard Example](docs/dashboard.gif)

---

## 🏗️ Architecture / Mermaid Diagram

This app is built on a modular, scalable stack:  
- **Frontend:** Bootstrap 5, Chart.js, custom JS/CSS, Jinja2 templates  
- **Backend:** Flask, Hugging Face LLMs, Sentence Transformers, spaCy, scikit-learn, pdfminer.six  
- **PDF Export:** pdfkit + wkhtmltopdf  
- **No DB:** All processing is in-memory/session for privacy

```mermaid
flowchart TD
  U[User] --> F[Frontend (Bootstrap, JS, Jinja2)]
  F --> B[Flask Backend]
  B -->|PDF/Text| X[Text Extraction]
  B -->|NLP| S[Skill Extraction (spaCy)]
  B -->|Embeddings| E[Semantic Scoring (SBERT)]
  B -->|LLM| L[Hugging Face Inference]
  B -->|ATS| A[ATS Checks]
  B --> D[Dashboard & PDF Export]
  style L fill:#f9f,stroke:#333,stroke-width:2px
  style E fill:#bbf,stroke:#333,stroke-width:2px
```

*Diagram: User uploads → frontend → backend → text extraction, skills, scoring, LLM feedback, ATS → dashboard & PDF. No persistent storage. All AI magic, no data hoarding.*

---

## 🤝 Contributing & Community

- **Fork, branch, PR:** Standard GitHub flow.  
- **Discussions:** Open issues for bugs/ideas.  
- **Code of Conduct:** Be kind, keep it constructive, respect all contributors.  
- **Docs:** See `/docs/` for diagrams, `/CONTRIBUTING.md` for guidelines.  
- **Open-source etiquette:** Let’s build something dope, but keep it professional. Your PRs shape the future—no gatekeeping.

---

## 📜 License & Support

- **License:** MIT — use, remix, and share.
- **Contact:** [project@yourdomain.com](mailto:project@yourdomain.com) or open an issue.
- **Feedback:** Always welcome—file issues, suggest features, or just vibe in the discussions.

---

## 📝 Footer / Additional Notes

- **Badges:** Keep them fresh—auto-update via CI.
- **Docs:** Store diagrams in `/docs/diagrams`, Mermaid `.mmd` files under version control.
- **Regenerate badges:** Set up in your pipeline.
- **Thanks for checking out Resume Reviewer.**  
  Keep it 100, and let’s make job search smarter for everyone.

---

*This README is alpha quality, just like the app. But with your help, it’ll be legendary. No cap.* 