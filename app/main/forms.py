from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField("Article Content", validators=[DataRequired()])
    SEO_link = StringField('SEO Link')
    submit = SubmitField('Submit')
