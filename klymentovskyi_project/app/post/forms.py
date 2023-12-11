from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import EnumType, Category

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
    category = SelectField("Category",
                           choices=list(map(lambda c : [c.id, c.name], Category.query.all())),
                           validators=[
                               DataRequired("Category is required.")
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
    category = SelectField("Category",
                           choices=list(map(lambda c : [c.id, c.name], Category.query.all())),
                           validators=[
                               DataRequired("Category is required.")
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

class CategoryCreationForm(FlaskForm):
    name = StringField("Name",
                        validators=[
                            Length(max=48),
                            DataRequired(message="Name is required.")
                        ])
    submit = SubmitField("Create")

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("Such category already exists.")

class CategoryUpdateForm(FlaskForm):
    def __init__(self, category: Category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._category = category

    name = StringField("Name",
                        validators=[
                            Length(max=48),
                            DataRequired(message="Name is required.")
                        ])
    submit = SubmitField("Update")

    def validate_name(self, field):
        if self._category.name == field.data:
            return

        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("Such category already exists.")
