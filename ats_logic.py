from jobs_data import jobs

# Master skill database
skills_db = [
    "python", "java", "c++", "sql",
    "machine learning", "data analysis",
    "excel", "django", "flask",
    "react", "javascript", "html", "css",
    "pandas", "numpy"
]


def extract_matched_skills(resume_text):
    matched = []
    for skill in skills_db:
        if skill in resume_text:
            matched.append(skill)
    return matched


def calculate_ats_score(resume_text):
    matched_skills = extract_matched_skills(resume_text)
    score = (len(matched_skills) / len(skills_db)) * 100
    return round(score, 2), matched_skills


def recommend_jobs(resume_text):
    recommendations = []

    for job in jobs:
        match_count = 0
        for skill in job["skills"]:
            if skill in resume_text:
                match_count += 1

        match_percent = (match_count / len(job["skills"])) * 100

        recommendations.append({
            "title": job["title"],
            "match": round(match_percent, 2)
        })

    # Sort by highest match
    recommendations.sort(key=lambda x: x["match"], reverse=True)

    return recommendations[:3]  # Top 3 jobs