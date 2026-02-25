import streamlit as st
from resume_parser import extract_text
from ats_logic import calculate_ats_score, recommend_jobs

st.set_page_config(page_title="Resume ATS Analyzer")

st.title("📄 Resume ATS Analyzer")
st.write("Upload your resume and get your ATS score with job recommendations.")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    score, matched_skills = calculate_ats_score(resume_text)
    recommendations = recommend_jobs(resume_text)

    st.subheader("📊 ATS Score")
    st.progress(int(score))
    st.write(f"Your ATS Score: {score} / 100")

    st.subheader("✅ Matched Skills")
    if matched_skills:
        for skill in matched_skills:
            st.write(f"- {skill}")
    else:
        st.write("No matching skills found.")

    st.subheader("💼 Top Job Recommendations")

    for job in recommendations:
        st.write(f"{job['title']} — Match: {job['match']}%")