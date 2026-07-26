import streamlit as st
from src.jobs import search_jobs
from src.ui import display_job_card
from src.rag import initialize_rag
from src.database import init_db
from src.saved_jobs import display_saved_jobs
from src.company_lookup import company_lookup

# Initialize RAG vector store and load career guide documents on startup
initialize_rag()

# Initialize SQLite database
init_db()

st.set_page_config(
    page_title="Job Search AI Agent",
    page_icon="💼",
    layout="wide"
)


page = st.sidebar.radio(
    "📂 Navigation",
    [
        "🔍 Job Search",
        "💾 Saved Jobs",
        "🏢 Company Lookup"
    ]
)

if page == "💾 Saved Jobs":
    display_saved_jobs()
    st.stop()

if page == "🏢 Company Lookup":
    company_lookup()
    st.stop()

if "jobs" not in st.session_state:
    st.session_state.jobs = []

st.title("💼 Job Search AI Agent")
st.write("Find jobs instantly using AI-powered search.")

# Resume Upload Section in the Sidebar
st.sidebar.subheader("📄 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

if uploaded_file is not None:
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    if (
        "last_uploaded_file" not in st.session_state
        or st.session_state.last_uploaded_file != uploaded_file.name
    ):
        with st.spinner("Processing resume and indexing for RAG..."):
            from src.rag import process_uploaded_resume

            resume_text = process_uploaded_resume(uploaded_file)
            st.session_state.resume_text = resume_text
            st.session_state.last_uploaded_file = uploaded_file.name
    else:
        resume_text = st.session_state.resume_text

    with st.expander("📄 Extracted Resume Text (Testing)"):
        if resume_text and not resume_text.startswith("Error"):
            st.text_area("Resume Plain Text", resume_text, height=300)
        else:
            st.warning("No text could be extracted from this PDF.")

st.sidebar.divider()
st.sidebar.subheader("🤖 AI Career Assistant")

import glob
import os

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

if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""


def on_suggested_select():
    sug = st.session_state.suggested_selectbox
    if sug != "-- Choose a suggested question --":
        st.session_state.chat_input = sug
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

selected_sug = st.sidebar.selectbox(
    "💡 Suggested Questions",
    ["-- Choose a suggested question --"] + suggested_questions,
    key="suggested_selectbox",
    on_change=on_suggested_select,
)

ask_button = st.sidebar.button(
    "🤖 Ask AI",
    use_container_width=True,
    type="primary",
)

if ask_button:
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
        st.markdown(f"**Q:** {st.session_state.last_question}")
        st.markdown(st.session_state.chat_response)

st.divider()

col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input(
        "🔍 Job Title",
        placeholder="e.g. Python Developer",
    )

with col2:
    location = st.text_input(
        "📍 Location",
        placeholder="e.g. Sangli, Remote",
    )

with st.expander("⚙️ Advanced Search Filters", expanded=False):
    col_f1, col_f2 = st.columns(2)

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
        keyword_filter = st.text_input(
            "🏢 Company Name (Optional)",
            placeholder="e.g. Amazon",
        )

st.write("")

if st.button(
    "🔍 Search Jobs",
    use_container_width=True,
    type="primary",
):
    query = job_title

    if location:
        query += f" jobs in {location}"

    with st.spinner("Searching..."):
        st.session_state.jobs = search_jobs(query)

filtered = []

for job in st.session_state.jobs:
    if employment_filter != "All":
        types = job.get("job_employment_types") or []

        if employment_filter not in types:
            continue

    if keyword_filter:
        employer = job.get("employer_name") or ""

        if keyword_filter.lower() not in employer.lower():
            continue

    filtered.append(job)

st.write("")

if filtered:
    st.subheader(f"💼 Match Results ({len(filtered)})")

    for job in filtered:
        display_job_card(job)

elif st.session_state.jobs:
    st.warning("⚠️ No jobs found matching the selected filters.")

else:
    st.info(
        "💡 Enter a job title and location above and click 'Search Jobs' to get started!"
    )