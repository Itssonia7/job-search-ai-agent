import streamlit as st
from src.jobs import search_jobs
from src.ui import display_job_card

def company_lookup():
    st.title("🏢 Company Lookup")

    company = st.text_input(
        "Enter Company Name",
        placeholder="Google, Amazon, Microsoft..."
    )

    if st.button("Search Company"):
        if company.strip():
            with st.spinner("Searching..."):
                jobs = search_jobs(company)

            if jobs:
                st.success(f"Found {len(jobs)} jobs")

                for job in jobs:
                    display_job_card(job)
            else:
                st.warning("No jobs found.")