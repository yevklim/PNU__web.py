from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ToDoForm(FlaskForm):
    task = StringField("Enter a task here",
                       validators=[
                           Length(max=80),
                           DataRequired(message="This field is required.")
                       ])
    description = StringField("Enter description",
                              validators=[
                                  Length(max=160),
                              ])
    submit = SubmitField("Save")
