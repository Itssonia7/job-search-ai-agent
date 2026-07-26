import hashlib
import streamlit as st
import sqlite3
from src.ai import analyze_job
from src.utils import format_salary

def save_job(job):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    salary = format_salary(job)

    try:
        cursor.execute(
            """
            INSERT INTO saved_jobs
            (job_title, company, location, employment, salary, apply_link)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                job.get("job_title"),
                job.get("employer_name"),
                job.get("job_city"),
                job.get("job_employment_type"),
                salary,
                job.get("job_apply_link"),
            ),
        )

        conn.commit()
        st.success("✅ Job saved successfully!")

    except sqlite3.IntegrityError:
        st.warning("⚠️ This job is already saved.")

    finally:
        conn.close()

def display_job_card(job):
    title = job.get("job_title", "N/A")
    company = job.get("employer_name", "N/A")
    city = job.get("job_city") or "Not specified"
    employment = job.get("job_employment_type", "N/A")
    apply_link = job.get("job_apply_link")

    salary = format_salary(job)

    unique_key = hashlib.md5(
        f"{title}_{company}_{city}_{apply_link}".encode("utf-8")
    ).hexdigest()

    with st.container(border=True):

        col1, col2, col3 = st.columns([5, 1, 1])

        with col1:
            st.subheader(title)
            st.write(f"🏢 **Company:** {company}")
            st.write(f"📍 **Location:** {city}")
            st.write(f"💼 **Employment:** {employment}")
            st.write(f"💰 **Salary:** {salary}")

        with col2:
            if apply_link:
                st.link_button("Apply", apply_link)

        with col3:
            if st.button("💾 Save", key=f"save_{unique_key}"):
               save_job(job)

        col_b1, col_b2 = st.columns(2) if st.session_state.get("resume_text") else (st.columns(1) + [None])

        with col_b1:
            if st.button("✨ Analyze with AI", key=f"ai_{unique_key}", use_container_width=True):
                with st.spinner("Analyzing with Gemini..."):
                    analysis = analyze_job(job)
                st.markdown(analysis)

        if col_b2 is not None:
            with col_b2:
                if st.button("📊 Analyze Resume Fit", key=f"fit_{unique_key}", use_container_width=True):
                    from src.ai import analyze_resume_match
                    with st.spinner("Matching resume with Gemini..."):
                        fit_analysis = analyze_resume_match(st.session_state.resume_text, job)
                    display_resume_analysis(fit_analysis)

        description = job.get("job_description")

        if description:
            with st.expander("Job Description"):
                st.write(description)


def display_resume_analysis(analysis_text):
    """Parses and renders the Gemini resume-to-job analysis output with a premium Streamlit UI."""
    import re

    sections = {
        "score": "",
        "matching_skills": "",
        "missing_skills": "",
        "improvements": "",
        "roadmap": "",
        "questions": ""
    }

    patterns = {
        "score": [r"##\s*(?:1\.)?\s*Match\s*Score", r"Match\s*Score"],
        "matching_skills": [r"##\s*(?:2\.)?\s*Matching\s*Skills", r"Matching\s*Skills"],
        "missing_skills": [r"##\s*(?:3\.)?\s*Missing\s*Skills", r"Missing\s*Skills"],
        "improvements": [r"##\s*(?:4\.)?\s*Resume\s*Improvements", r"Resume\s*Improvements"],
        "roadmap": [r"##\s*(?:5\.)?\s*Learning\s*Roadmap", r"Learning\s*Roadmap"],
        "questions": [r"##\s*(?:6\.)?\s*Interview\s*Questions", r"Interview\s*Questions"]
    }

    headers_found = []
    for key, regexes in patterns.items():
        for regex in regexes:
            match = re.search(regex, analysis_text, re.IGNORECASE)
            if match:
                headers_found.append((key, match.start(), match.end()))
                break

    headers_found.sort(key=lambda x: x[1])

    for i in range(len(headers_found)):
        key, start, end = headers_found[i]
        next_start = headers_found[i+1][1] if i + 1 < len(headers_found) else len(analysis_text)
        content = analysis_text[end:next_start].strip()
        sections[key] = content

    st.write("")
    st.markdown("---")
    st.subheader("📊 Resume Match Analysis")

    # Render Match Score Section
    if sections["score"]:
        score_match = re.search(r"(\d+)\s*/\s*100", sections["score"], re.IGNORECASE)
        if not score_match:
            score_match = re.search(r"Score:\s*(\d+)", sections["score"], re.IGNORECASE)

        score_value = int(score_match.group(1)) if score_match else 50

        col_metric, col_prog = st.columns([1, 2])
        with col_metric:
            st.metric(
                label="Match Score",
                value=f"{score_value}/100",
                delta=f"{score_value - 50}% vs passing score" if score_value >= 50 else f"{score_value - 50}% vs passing score",
                delta_color="normal" if score_value >= 60 else "inverse"
            )
        with col_prog:
            st.write("")  # Spacer to vertically center the progress bar
            st.progress(score_value / 100.0)

        # Display score explanation
        explanation = re.sub(r"Score:\s*\d+/\d+", "", sections["score"], flags=re.IGNORECASE).strip()
        st.markdown(explanation)

    st.write("")

    # Render Skills & Missing Skills side-by-side in columns
    col_skills_1, col_skills_2 = st.columns(2)
    with col_skills_1:
        with st.container(border=True):
            st.markdown("#### 🟢 Matching Skills")
            st.markdown(sections["matching_skills"] if sections["matching_skills"] else "No matching skills identified.")
    with col_skills_2:
        with st.container(border=True):
            st.markdown("#### 🔴 Missing Skills")
            st.markdown(sections["missing_skills"] if sections["missing_skills"] else "No missing skills identified.")

    st.write("")

    # Render improvements, roadmap, and questions in clean expanders
    if sections["improvements"]:
        with st.expander("💡 Actionable Resume Improvements", expanded=True):
            st.markdown(sections["improvements"])

    if sections["roadmap"]:
        with st.expander("📚 Bridge the Gaps: Learning Roadmap", expanded=False):
            st.markdown(sections["roadmap"])

    if sections["questions"]:
        with st.expander("💬 Tailored Interview Preparation Questions", expanded=False):
            st.markdown(sections["questions"])