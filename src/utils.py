def format_salary(job):
    """
    Convert salary to Indian LPA format.
    """

    min_salary = job.get("job_min_salary")
    max_salary = job.get("job_max_salary")

    if not min_salary and not max_salary:
        return "Salary Not Disclosed"

    if min_salary and max_salary:
        return f"₹ {min_salary/100000:.1f} - ₹ {max_salary/100000:.1f} LPA"

    if min_salary:
        return f"₹ {min_salary/100000:.1f} LPA"

    return f"₹ {max_salary/100000:.1f} LPA"