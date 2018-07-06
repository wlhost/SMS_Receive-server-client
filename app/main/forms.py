from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField


class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')
