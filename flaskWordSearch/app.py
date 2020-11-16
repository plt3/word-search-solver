import json
import os
import time

from flask import Flask, redirect, render_template, request, url_for

from forms import urlForm
from utils import findWords, getGridAndList, getHtml, getTitle

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("WORD_SEARCH_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    form = urlForm()
    if form.validate_on_submit():
        return redirect(url_for("wordSearchPage", url=form.url.data))
    return render_template("form.html", form=form, timeStamp=time.time())


@app.route("/puzzle")
def wordSearchPage():
    fullUrl = "http://www.whenwewordsearch.com/word_search/" + request.args.get("url")
    try:
        pageContent = getHtml(fullUrl)

        fullGrid, wordsList = getGridAndList(pageContent)
        title = getTitle(pageContent)
    except Exception:
        return "ERROR: url parameter is not valid link to puzzle."
    resultDict = findWords(fullGrid, wordsList)

    return render_template(
        "puzzle.html",
        title=title,
        grid=fullGrid,
        words=wordsList,
        resDict={word: json.dumps(resultDict[word]) for word in resultDict.keys()},
        timeStamp=time.time(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
