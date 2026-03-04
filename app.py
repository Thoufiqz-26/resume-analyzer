from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]
    text = extract_text_from_pdf(file)

    word_count = len(text.split())

    return render_template("result.html", words=word_count)

if __name__ == "__main__":
    app.run()