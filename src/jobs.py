import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Read from Streamlit Secrets first, then .env
API_KEY = st.secrets.get("RAPIDAPI_KEY", os.getenv("RAPIDAPI_KEY"))
API_HOST = st.secrets.get("RAPIDAPI_HOST", os.getenv("RAPIDAPI_HOST", "jsearch.p.rapidapi.com"))


MOCK_JOBS = [
    {
        "job_id": "mock_1",
        "job_title": "Software Engineer",
        "employer_name": "Google",
        "job_city": "Bangalore",
        "job_employment_type": "Full-time",
        "job_employment_types": ["FULLTIME"],
        "job_apply_link": "https://careers.google.com",
        "job_min_salary": 1800000,
        "job_max_salary": 3500000,
        "job_description": "We are seeking a Software Engineer to design, develop, and deploy large-scale software solutions. You will work on cutting-edge systems, collaborate with cross-functional teams, and solve complex algorithms."
    },
    {
        "job_id": "mock_2",
        "job_title": "Python Developer",
        "employer_name": "Amazon",
        "job_city": "Sangli",
        "job_employment_type": "Full-time",
        "job_employment_types": ["FULLTIME"],
        "job_apply_link": "https://amazon.jobs",
        "job_min_salary": 1200000,
        "job_max_salary": 2400000,
        "job_description": "Looking for a Python Developer to join our Amazon Web Services (AWS) team in Sangli. Responsibilities include building scalable web services, working with cloud infrastructure, and writing clean, maintainable backend code."
    },
    {
        "job_id": "mock_3",
        "job_title": "Data Analyst Intern",
        "employer_name": "TCS",
        "job_city": "Mumbai",
        "job_employment_type": "Internship",
        "job_employment_types": ["INTERN"],
        "job_apply_link": "https://tcs.com/careers",
        "job_min_salary": 15000,
        "job_max_salary": 25000,
        "job_description": "Join our data analytics division as an intern. You will perform data cleaning, build visualization dashboards using Tableau/PowerBI, and write SQL/Python queries to extract business insights."
    },
    {
        "job_id": "mock_4",
        "job_title": "React Frontend Developer",
        "employer_name": "Infosys",
        "job_city": "Pune",
        "job_employment_type": "Contractor",
        "job_employment_types": ["CONTRACTOR"],
        "job_apply_link": "https://infosys.com/careers",
        "job_min_salary": 800000,
        "job_max_salary": 1400000,
        "job_description": "We need a contract-based Frontend Developer proficient in React, Redux, and Tailwind CSS. You will build modern user interfaces, optimize web performance, and integrate REST APIs."
    },
    {
        "job_id": "mock_5",
        "job_title": "AI Research Engineer",
        "employer_name": "OpenAI",
        "job_city": "Remote",
        "job_employment_type": "Full-time",
        "job_employment_types": ["FULLTIME"],
        "job_apply_link": "https://openai.com/careers",
        "job_min_salary": 2500000,
        "job_max_salary": 5000000,
        "job_description": "Work on the frontier of artificial intelligence. Design and train large-scale neural networks, optimize training runs, and collaborate with leading scientists to shape the future of technology."
    }
]

def fetch_jobs_from_api(query):
    url = f"https://{API_HOST}/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    params = {
        "query": query,
        "page": 1,
        "num_pages": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data.get("data", [])


def filter_jobs(jobs, work_mode="Any", notice_period="Any"):
    # Currently no additional filtering.
    # The API query itself handles Remote/Hybrid searches.
    return jobs


def search_jobs(query):
    try:
        jobs = fetch_jobs_from_api(query)

    except Exception as e:
        st.warning(f"⚠️ API Access Error: {e}")
        st.info("Using mock jobs.")

        query_lower = query.lower()

        jobs = [
            job
            for job in MOCK_JOBS
            if query_lower in job["job_title"].lower()
            or query_lower in job["employer_name"].lower()
            or query_lower in job["job_city"].lower()
        ]

        if not jobs:
            jobs = MOCK_JOBS

    return jobs