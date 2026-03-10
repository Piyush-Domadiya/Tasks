from flask import Flask, render_template, request
import os
from pdfminer.high_level import extract_text
from model import get_score
from skills import extract_skills

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # PDF se text extract
    text = extract_text(filepath)

    job_desc = request.form["job"]

    # similarity score
    score = get_score(text, job_desc)

    # skills detection
    skills = extract_skills(text)

    return render_template("index.html", result=score, skills=skills)


if __name__ == "__main__":
    app.run(debug=True)