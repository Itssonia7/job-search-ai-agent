import glob
import os

import streamlit as st

from src.company_lookup import company_lookup
from src.database import init_db
from src.jobs import search_jobs
from src.rag import initialize_rag
from src.saved_jobs import display_saved_jobs
from src.ui import display_job_card


# ---------------------------------------------------
# Initialization
# ---------------------------------------------------

initialize_rag()
init_db()

st.set_page_config(
    page_title="💼 Job Search AI Agent",
    page_icon="💼",
    layout="wide",
)

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------

page = st.sidebar.radio(
    "📂 Navigation",
    [
        "🔍 Job Search",
        "💾 Saved Jobs",
        "🏢 Company Lookup",
    ],
)

if page == "💾 Saved Jobs":
    display_saved_jobs()
    st.stop()

if page == "🏢 Company Lookup":
    company_lookup()
    st.stop()

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "jobs" not in st.session_state:
    st.session_state.jobs = []

if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("💼 Job Search AI Agent")
st.write("Find jobs instantly using AI-powered search.")

# ---------------------------------------------------
# Resume Upload
# ---------------------------------------------------

st.sidebar.subheader("📄 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"],
)

if uploaded_file is not None:

    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    if (
        "last_uploaded_file" not in st.session_state
        or st.session_state.last_uploaded_file != uploaded_file.name
    ):

        with st.spinner("Processing resume..."):

            from src.rag import process_uploaded_resume

            resume_text = process_uploaded_resume(uploaded_file)

            st.session_state.resume_text = resume_text
            st.session_state.last_uploaded_file = uploaded_file.name

    else:

        resume_text = st.session_state.resume_text

    with st.expander("📄 Extracted Resume Text"):

        if resume_text and not resume_text.startswith("Error"):

            st.text_area(
                "Resume",
                resume_text,
                height=300,
            )

        else:

            st.warning("No text could be extracted.")

# ---------------------------------------------------
# AI Career Assistant
# ---------------------------------------------------

st.sidebar.divider()
st.sidebar.subheader("🤖 AI Career Assistant")

pdf_files = glob.glob(os.path.join("documents", "*.pdf"))

has_pdfs = len(pdf_files) > 0

has_resume = (
    "resume_text" in st.session_state
    and st.session_state.resume_text is not None
)

if not has_pdfs:
    st.sidebar.warning("⚠️ No knowledge documents found.")

if not has_resume:
    st.sidebar.warning("⚠️ Upload your resume first.")


def on_suggested_select():

    suggestion = st.session_state.suggested_selectbox

    if suggestion != "-- Choose a suggested question --":

        st.session_state.chat_input = suggestion
        st.session_state.suggested_selectbox = (
            "-- Choose a suggested question --"
        )


user_question = st.sidebar.text_input(
    "Ask anything about Resume, Jobs, Interview, Career, Learning:",
    key="chat_input",
)

suggested_questions = [
    "Should I apply for this job?",
    "Improve my resume.",
    "Which skills am I missing?",
    "Prepare interview questions.",
    "Learning roadmap.",
    "Career advice.",
]

st.sidebar.selectbox(
    "💡 Suggested Questions",
    ["-- Choose a suggested question --"] + suggested_questions,
    key="suggested_selectbox",
    on_change=on_suggested_select,
)

if st.sidebar.button(
    "🤖 Ask AI",
    use_container_width=True,
    type="primary",
):

    if not has_resume:

        st.sidebar.error("Upload your resume first.")

    elif not has_pdfs:

        st.sidebar.error("No knowledge documents found.")

    elif not user_question.strip():

        st.sidebar.warning("Please enter a question.")

    else:

        with st.sidebar.spinner("Generating response..."):

            from src.chatbot import career_chat

            response = career_chat(user_question)

            st.session_state.chat_response = response
            st.session_state.last_question = user_question

if "chat_response" in st.session_state:

    with st.sidebar.container(border=True):

        st.markdown(
            f"**Q:** {st.session_state.last_question}"
        )

        st.markdown(
            st.session_state.chat_response
        )

st.divider()

# ---------------------------------------------------
# Job Search
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input(
        "🔍 Job Title",
        placeholder="e.g. Python Developer",
    )

with col2:
    location = st.text_input(
        "📍 Location",
        placeholder="e.g. Pune",
    )

with st.expander("⚙️ Advanced Search Filters", expanded=False):

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        employment_filter = st.selectbox(
            "💼 Employment Type",
            [
                "All",
                "FULLTIME",
                "PARTTIME",
                "CONTRACTOR",
                "INTERN",
            ],
        )

    with col_f2:
        work_mode = st.selectbox(
            "🏠 Work Mode",
            [
                "Any",
                "Remote",
                "Hybrid",
                "On-site",
            ],
        )

    with col_f3:
        notice_period = st.selectbox(
            "⏳ Notice Period",
            [
                "Any",
                "Immediate",
                "15 Days",
                "30 Days",
                "60 Days",
                "90 Days",
            ],
        )

    keyword_filter = st.text_input(
        "🏢 Company Name (Optional)",
        placeholder="e.g. Google",
    )

st.write("")

# ---------------------------------------------------
# Search Button
# ---------------------------------------------------

if st.button(
    "🔍 Search Jobs",
    use_container_width=True,
    type="primary",
):

    if not job_title.strip():
        st.warning("Please enter a job title.")
        st.stop()

    query = job_title.strip()

    # Location
    if location.strip():
        query += f" jobs in {location.strip()}"
    else:
        query += " jobs in India"

    # Work Mode
    if work_mode == "Remote":
        query += " remote"

    elif work_mode == "Hybrid":
        query += " hybrid"

    # Future feature
    # Notice Period isn't supported by the API yet.

    with st.spinner("Searching jobs..."):

        st.session_state.jobs = search_jobs(query)

# ---------------------------------------------------
# Local Filters
# ---------------------------------------------------

filtered = []

for job in st.session_state.jobs:

    if employment_filter != "All":

        job_types = job.get("job_employment_types") or []

        if employment_filter not in job_types:
            continue

    if keyword_filter:

        employer = job.get("employer_name", "")

        if keyword_filter.lower() not in employer.lower():
            continue

    filtered.append(job)

st.write("")

# ---------------------------------------------------
# Results
# ---------------------------------------------------

if filtered:

    st.subheader(f"💼 Match Results ({len(filtered)})")

    for job in filtered:
        display_job_card(job)

elif st.session_state.jobs:

    st.warning(
        "⚠️ No jobs found matching the selected filters."
    )

else:

    st.info(
        "💡 Enter a job title and click 'Search Jobs' to get started!"
    )