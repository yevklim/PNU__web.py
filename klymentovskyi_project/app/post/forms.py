from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, BooleanField, SubmitField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Length, ValidationError
from .models import EnumType, Category, Tag

class PostCreationForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(-1, ''), *((c.id, c.name) for c in Category.query.all())]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.all()]

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
    category = SelectField("Category", coerce=int)
    type = SelectField("Type",
                       choices=list(map(lambda i : [i.name, i.label], EnumType)),
                       validators=[
                           DataRequired("Type is required.")
                       ])
    tags = SelectMultipleField("Tags", coerce=int)
    enabled = BooleanField("Enabled")
    submit = SubmitField("Publish")

class PostUpdateForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(-1, ''), *((c.id, c.name) for c in Category.query.all())]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.all()]

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
    category = SelectField("Category", coerce=int)
    type = SelectField("Type",
                       choices=list(map(lambda i : [i.name, i.label], EnumType)),
                       validators=[
                           DataRequired("Type is required.")
                       ])
    tags = SelectMultipleField("Tags", coerce=int)
    # tags = SelectMultipleField("Tags")
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


class TagCreationForm(FlaskForm):
    name = StringField("Name",
                        validators=[
                            Length(max=48),
                            DataRequired(message="Name is required.")
                        ])
    submit = SubmitField("Create")

    def validate_name(self, field):
        if Tag.query.filter_by(name=field.data).first():
            raise ValidationError("Such tag already exists.")

class TagUpdateForm(FlaskForm):
    def __init__(self, tag: Tag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tag = tag

    name = StringField("Name",
                        validators=[
                            Length(max=48),
                            DataRequired(message="Name is required.")
                        ])
    submit = SubmitField("Update")

    def validate_name(self, field):
        if self._tag.name == field.data:
            return

        if Tag.query.filter_by(name=field.data).first():
            raise ValidationError("Such tag already exists.")
