from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "quick test ftb"


if __name__ == "__main__":
    app.run(debug=True)
