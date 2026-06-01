import streamlit as st
import pdfplumber

st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide"
)

SKILLS_DATABASE = [
    "python",
    "c++",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "git",
    "github",
    "aws",
    "api",
    "machine learning",
    "artificial intelligence",
    "prompt engineering",
    "data structures",
    "algorithms",
    "oop",
    "backend",
    "frontend",
    "mongodb",
    "mysql",
    "streamlit",
    "flask"
]


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DATABASE:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def recommend_roles(skills):
    roles = []

    if "python" in skills and "machine learning" in skills:
        roles.append("AI Engineer")

    if "python" in skills and "sql" in skills:
        roles.append("Data Analyst")

    if "html" in skills and "css" in skills and "javascript" in skills:
        roles.append("Frontend Developer")

    if "backend" in skills or "api" in skills:
        roles.append("Backend Developer")

    if "prompt engineering" in skills:
        roles.append("AI Research Assistant")

    if not roles:
        roles.append("Software Developer")

    return roles


st.title("Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if uploaded_file:

    resume_text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                resume_text += page_text

    st.subheader("Resume Preview")

    st.text_area(
        "",
        resume_text[:3000],
        height=200
    )

    resume_skills = extract_skills(resume_text)

    st.subheader("Detected Resume Skills")

    if resume_skills:
        st.write(sorted(resume_skills))
    else:
        st.write("No skills detected.")

    if job_description:

        job_skills = extract_skills(job_description)

        matched_skills = list(
            set(resume_skills).intersection(set(job_skills))
        )

        missing_skills = list(
            set(job_skills) - set(resume_skills)
        )

        if len(job_skills) > 0:
            ats_score = (
                len(matched_skills)
                / len(job_skills)
            ) * 100
        else:
            ats_score = 0

        st.subheader("ATS Match Score")

        st.progress(int(ats_score))

        st.write(
            f"{round(ats_score, 2)}%"
        )

        st.subheader("Matched Skills")

        if matched_skills:
            st.write(sorted(matched_skills))
        else:
            st.write("No matching skills found.")

        st.subheader("Missing Skills")

        if missing_skills:
            st.write(sorted(missing_skills))
        else:
            st.write("No major skill gaps detected.")

        st.subheader("Suggested Career Roles")

        roles = recommend_roles(
            resume_skills
        )

        for role in roles:
            st.write(f"- {role}")

        st.subheader("Learning Roadmap")

        if missing_skills:
            for skill in missing_skills:
                st.write(
                    f"Learn {skill} to improve compatibility with this role."
                )
        else:
            st.write(
                "Your skill set aligns well with the job requirements."
            )