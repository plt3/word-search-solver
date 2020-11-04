import requests
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError


class urlForm(FlaskForm):
    url = StringField(label="Enter URL here:")
    submit = SubmitField()

    def validate_url(self, url):
        if not (url.data.startswith("http://") or url.data.startswith("https://")):
            goodPrefix = ""
            for prefix in ["http://", "https://"]:
                try:
                    requests.get(prefix + url.data)
                    goodPrefix = prefix
                    break
                except ConnectionError:
                    pass

            if not goodPrefix:
                raise ValidationError("Please enter a valid URL.")
            else:
                url.data = goodPrefix + url.data
