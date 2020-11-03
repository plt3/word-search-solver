from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField


class urlForm(FlaskForm):
    url = TextField(label="Enter URL here:")
    submit = SubmitField(label="Submit")
