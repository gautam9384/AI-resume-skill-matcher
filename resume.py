import streamlit as st
from tempfile import NamedTemporaryFile
from fuzzywuzzy import fuzz
import spacy
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


nlp = spacy.load("en_core_web_sm")

# basic skillset
SKILL_SET = [
    'python', 'java', 'c++', 'sql', 'machine learning', 'data analysis',
    'tensorflow', 'keras', 'nlp', 'deep learning', 'excel', 'pandas',
    'numpy', 'communication', 'teamwork', 'problem solving'
]

def extract_skills(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc]
    extracted_skills = [skill for skill in SKILL_SET if skill in tokens]
    return list(set(extracted_skills))



def calculate_match(resume_skills, job_skills):
    match_count = 0
    for skill in job_skills:
        for res_skill in resume_skills:
            if fuzz.partial_ratio(skill.lower(), res_skill.lower()) > 80:
                match_count += 1
                break
    score = (match_count / len(job_skills)) * 100
    return round(score, 2)


st.title("📄 AI Resume Skill Matcher")
st.write("Upload your resume and job description to see the match score.")

resume_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
job_desc = st.text_area("Paste Job Description Here")

if resume_file and job_desc:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.read())
        resume_text = extract_text_from_pdf(tmp.name)
    
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    score = calculate_match(resume_skills, job_skills)

    st.subheader("Results")
    st.write("**Extracted Resume Skills:**", resume_skills)
    st.write("**Extracted Job Skills:**", job_skills)
    st.write(f"**Match Score:** {score} %")
