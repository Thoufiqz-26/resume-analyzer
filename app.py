from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Simple skill keywords
SKILLS = [
    "python", "java", "c++", "machine learning",
    "data analysis", "flask", "django", "sql",
    "html", "css", "javascript"
]

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]
    text = extract_text_from_pdf(file)

    # Word count
    word_count = len(text.split())

    # Skill matching
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    score = len(found_skills) * 10

    if score >= 50:
        feedback = "Excellent Resume 👍"
    elif score >= 30:
        feedback = "Good Resume 🙂"
    else:
        feedback = "Needs Improvement ⚠"

    return render_template(
        "result.html",
        words=word_count,
        skills=found_skills,
        score=score,
        feedback=feedback
    )

if __name__ == "__main__":
    app.run()