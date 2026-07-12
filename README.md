# 💼 AI Job Search Assistant & Resume Analyzer

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-Powered-orange.svg)](https://deepmind.google/technologies/gemini/)

An intelligent, end-to-end career assistant that allows job seekers to query active jobs, filter matches, upload resumes, and receive instant AI-powered ATS alignment analyses, learning roadmaps, and custom interview prep questions.

---

## 📌 Problem Statement

Finding the right job in today's market is a dual challenge:
1. **Search Fragmentation**: Querying multiple job boards is tedious, and filtering through job posts for specific employment types or companies is time-consuming.
2. **The ATS Black Box**: Over 70% of resumes are filtered out by Applicant Tracking Systems (ATS) before reaching human eyes. Job seekers often apply to roles without knowing if their resume matches the job description, what keywords they are missing, or how to prepare for specific interviews.

The **AI Job Search Assistant** bridges this gap by combining live job search indexing with an instant, interactive resume-matching feedback loop.

---

## ✨ Features

- **Live Job Search**: Fetch real-time job listings using the JSearch API (with built-in offline mock fallbacks for testing).
- **Advanced Filtering**: Instantly refine listings by employment types (Full-time, Intern, Contractor, etc.) or specific companies.
- **In-Memory PDF Parser**: Upload and parse PDF resumes on-the-fly without saving sensitive user documents to disk.
- **Deterministic UI Rendering**: Uses cryptographic hashing for Streamlit widgets to guarantee stable state loads across user interactions.
- **Premium Resume Matcher (Gemini 3.5 Flash)**:
  - **Match Score (0-100)**: Visual progress indicator showing resume-to-job compatibility.
  - **Side-by-Side Skill Mapping**: Clear comparison of matching vs. missing skills/keywords.
  - **Actionable Feedback**: Precise phrasing and structure tips to bypass ATS filters.
  - **Bridge-the-Gap Learning Roadmap**: Weekly learning timeline for missing technical skills.
  - **Tailored Interview Prep**: Custom interview questions with structured answer guidelines.

---

## 🛠️ Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Large Language Model**: [Google Gemini 3.5 Flash](https://deepmind.google/technologies/gemini/)
- **PDF Extraction**: [PyPDF2](https://pypi.org/project/PyPDF2/)
- **HTTP client**: [Requests](https://psf.github.io/requests/)
- **Environment Management**: [Python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📁 Folder Structure

```text
job-search-ai-agent/
├── .streamlit/
│   └── secrets.toml          # Streamlit secrets (API keys)
├── src/
│   ├── ai.py                 # Gemini LLM integration & prompt engineering
│   ├── jobs.py               # Job search API client & mock database fallback
│   ├── pdf_reader.py         # PyPDF2 file stream parsing utilities
│   ├── ui.py                 # Job card rendering & parsed analysis report UI
│   └── __init__.py
├── app.py                    # Main Streamlit application entrypoint
├── requirements.txt          # Python package dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- A Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))
- A RapidAPI JSearch Key (Optional, fallback mock data is enabled by default)

### 1. Clone the Repository
```bash
git clone https://github.com/Itssonia7/job-search-ai-agent.git
cd job-search-ai-agent
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Secrets
Create a secrets file under `.streamlit/secrets.toml`:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"      # Optional
```

### 5. Launch the Application
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## 📸 Screenshots

| Onboarding & Search Dashboard | Premium ATS Analysis Report |
| :---: | :---: |
| *[Insert Search Screenshot]* | *[Insert Analysis Report Screenshot]* |

---

## 🔮 Future Scope

- **ATS Resume Match Score Tracker**: Maintain a history of matched scores to trace portfolio improvement.
- **Auto-Generated Cover Letters**: Generate tailored cover letters aligned with matching skills.
- **Multi-Format Upload Support**: Enable parsing for Docx and TXT resumes.
- **Email Job Alerts**: Automatically email matching job opportunities to users.