import time

from flask import Flask, redirect, render_template, request, url_for

from forms import urlForm
from utils import findWords, getGridAndList, getHtml

app = Flask(__name__)
app.config["SECRET_KEY"] = "M-{4;:66>_0E%ziF%y)#m<Rye#Y5&RU{[&24y,<9"


@app.route("/", methods=["GET", "POST"])
def home():
    form = urlForm()
    if form.validate_on_submit():
        return redirect(url_for("wordSearchPage", url=form.url.data))
    return render_template("form.html", form=form, timeStamp=time.time())


@app.route("/puzzle")
def wordSearchPage():
    # return request.args.get("url")
    pageContent = getHtml(request.args.get("url"))
    fullGrid, wordsList = getGridAndList(pageContent)
    # resultDict = findWords(fullGrid, wordsList)
    return render_template("puzzle.html", grid=fullGrid, words=wordsList)


if __name__ == "__main__":
    app.run(debug=True)
