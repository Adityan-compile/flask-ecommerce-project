from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("index.html", title="home", content="Hello")


if "__name__" == "__main__":
    app.run(debug="true")
