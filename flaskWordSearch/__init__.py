import os

from flask import Flask, redirect, render_template, request, url_for

from flaskWordSearch.forms import urlForm
from flaskWordSearch.utils import findWords, getGridAndList, getHtml, getTitle

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("WORD_SEARCH_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    form = urlForm()
    if form.validate_on_submit():
        return redirect(url_for("wordSearchPage", url=form.url.data))
    return render_template("form.html", form=form)


@app.route("/puzzle")
def wordSearchPage():
    urlParam = request.args.get("url")

    try:
        if not urlParam.startswith("http://www.whenwewordsearch.com/word_search/"):
            urlParam = "http://www.whenwewordsearch.com/word_search/" + urlParam
    except AttributeError:
        return (
            render_template(
                "error.html",
                error='400 ERROR: no "url" query parameter passed',
            ),
            400,
        )
    try:
        pageContent = getHtml(urlParam)

        fullGrid, wordsList = getGridAndList(pageContent)
        title = getTitle(pageContent)
    except Exception:
        return (
            render_template(
                "error.html", error="404 ERROR: we couldn't find a puzzle at that link."
            ),
            404,
        )

    return render_template(
        "puzzle.html",
        title=title,
        grid=fullGrid,
        words=wordsList,
    )


@app.route("/api/solvePuzzle", methods=["GET"])
def jsonSolve():
    """
    Small API that takes a "url" query parameter of the page to a word search puzzle
    and returns a JSON string of the words to find and their starting points and
    directions
    """

    urlParam = request.args.get("url")

    try:
        if not urlParam.startswith("http://www.whenwewordsearch.com/word_search/"):
            urlParam = "http://www.whenwewordsearch.com/word_search/" + urlParam
    except AttributeError:
        return {
            "ERROR": 'Please pass query parameter called "url" with url of puzzle'
        }, 400
    try:
        pageContent = getHtml(urlParam)

        fullGrid, wordsList = getGridAndList(pageContent)
    except Exception:
        return {"ERROR": "url parameter is not valid link to puzzle."}, 404

    return findWords(fullGrid, wordsList)
