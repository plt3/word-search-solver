from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError

from flaskWordSearch.utils import getGridAndList, getHtml


class urlForm(FlaskForm):
    url = StringField(label="Enter URL here:")
    submit = SubmitField()

    def validate_url(self, url):
        # make sure to add http://www. to every url that gets entered
        if url.data.startswith("http://"):
            url.data = url.data[7:]

        if url.data.startswith("www."):
            url.data = url.data[4:]

        url.data = "http://www." + url.data

        if not url.data.startswith("http://www.whenwewordsearch.com/word_search/"):
            raise ValidationError(
                "Please enter a link to a word search page on the provided website"
            )

        try:
            pageContent = getHtml(url.data)
            getGridAndList(pageContent)
        except Exception:
            # any errors at getting grid and words means that URL was invalid
            raise ValidationError("Please enter a valid URL on the provided website.")

        # just pass last part of URL to next page to shorten query parameters
        url.data = url.data[44:]
