from flask import Flask, render_template, request
from get_image import getImageURL
from extract import extract_informations_from_text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main.html", errors_count = -1)
    if request.method == "POST":
        text = request.form.get("text")
        commands, object_summaries, condition_summaries = extract_informations_from_text(text)
        print(commands)
        imageURL = getImageURL(commands)
        return render_template("main.html", imageURL=imageURL, problem=text, object_summaries=object_summaries, condition_summaries=condition_summaries,
                                objects="Objects:", conditions="Conditions:")


