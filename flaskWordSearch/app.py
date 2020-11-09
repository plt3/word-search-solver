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
    # fullUrl = "http://www.whenwewordsearch.com/word_search/" + request.args.get("url")
    try:
        # pageContent = getHtml(fullUrl)

        # delete this when ready to actually run server
        with open("warof1812.html") as f:
            pageContent = f.read()
        # end delete block

        fullGrid, wordsList = getGridAndList(pageContent)
    except Exception:
        return "ERROR: url parameter is not valid link to puzzle."
    resultDict = findWords(fullGrid, wordsList)
    return render_template(
        "puzzle.html",
        grid=fullGrid,
        words=wordsList,
        # turning all the lists into strings is shameful. Better way to do this???
        resDict={word: str(resultDict[word]) for word in resultDict.keys()},
        timeStamp=time.time(),
    )


if __name__ == "__main__":
    app.run(debug=True)
