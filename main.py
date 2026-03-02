import PyPDF2
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# Load predefined skills
def load_skills():
    with open("skills.txt", "r") as f:
        return [skill.strip().lower() for skill in f.readlines()]

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()

# Extract skills from text
def extract_skills(text, skills_list):
    found_skills = []
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
    return found_skills

# Calculate match score
def calculate_match(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    score = (vectors * vectors.T).toarray()[0][1]
    return round(score * 100, 2)


def main():
    print("==== AI Resume Analyzer ====")

    skills_list = load_skills()

    resume_path = input("Enter resume PDF path: ")
    resume_text = extract_text_from_pdf(resume_path)

    job_description = input("Paste Job Description: ").lower()

    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_description, skills_list)

    match_score = calculate_match(resume_text, job_description)

    missing_skills = list(set(job_skills) - set(resume_skills))

    print("\n===== RESULTS =====")
    print("Match Score:", match_score, "%")
    print("Skills in Resume:", resume_skills)
    print("Skills Required:", job_skills)
    print("Missing Skills:", missing_skills)


if __name__ == "__main__":
    main()