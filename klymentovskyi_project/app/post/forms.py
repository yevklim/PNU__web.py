from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from .models import EnumType

class PostCreationForm(FlaskForm):
    title = StringField("Title",
                        validators=[
                            Length(max=64),
                            DataRequired(message="Title is required.")
                        ])
    text = TextAreaField("Content",
                         validators=[
                             Length(max=1024),
                             DataRequired(message="Content is required.")
                         ])
    type = SelectField("Type",
                       choices=list(map(lambda i : [i.name, i.label], EnumType)),
                       validators=[
                           DataRequired("Type is required.")
                       ])
    enabled = BooleanField("Enabled")
    submit = SubmitField("Publish")

class PostUpdateForm(FlaskForm):
    title = StringField("Title",
                        validators=[
                            Length(max=64),
                            DataRequired(message="Title is required.")
                        ])
    text = TextAreaField("Content",
                         validators=[
                             Length(max=160),
                             DataRequired(message="Content is required.")
                         ])
    type = SelectField("Type",
                       choices=list(map(lambda i : [i.name, i.label], EnumType)),
                       validators=[
                           DataRequired("Type is required.")
                       ])
    enabled = BooleanField("Enabled")
    submit = SubmitField("Update")

class PostDeletionForm(FlaskForm):
    submit = SubmitField("Confirm Deletion", render_kw={ "category": "danger" })
