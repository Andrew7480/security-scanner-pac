from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open("report.json") as f:
            findings = json.load(f)
    except:
        findings = []
    return render_template("index.html", findings=findings)

if __name__ == "__main__":
    app.run(debug=True)
