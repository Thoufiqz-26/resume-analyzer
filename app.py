from flask import Flask, render_template, request
import PyPDF2
import nltk
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def calculate_similarity(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            score = calculate_similarity(resume_text, job_desc)

    return render_template("index.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)