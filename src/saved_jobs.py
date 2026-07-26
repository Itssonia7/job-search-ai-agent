import sqlite3
import streamlit as st

DB_NAME = "jobs.db"


def display_saved_jobs():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM saved_jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    st.title("💾 Saved Jobs")

    if not jobs:
        st.info("No saved jobs yet.")
        conn.close()
        return

    for job in jobs:
        with st.container(border=True):
            st.subheader(job["job_title"])
            st.write(f"🏢 Company: {job['company']}")
            st.write(f"📍 Location: {job['location']}")
            st.write(f"💼 Employment: {job['employment']}")
            st.write(f"💰 Salary: {job['salary']}")

            if job["apply_link"]:
                st.link_button("Apply", job["apply_link"])

            if st.button("🗑 Delete", key=f"delete_{job['id']}"):
                cursor.execute(
                    "DELETE FROM saved_jobs WHERE id=?",
                    (job["id"],)
                )
                conn.commit()
                st.success("Job deleted.")
                st.rerun()

    conn.close()