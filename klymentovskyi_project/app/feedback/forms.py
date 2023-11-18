from flask_wtf import FlaskForm
from wtforms import EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class FeedBackForm(FlaskForm):
    email = EmailField("E-mail",
                       validators=[
                           Length(max=256),
                           Email(message="Incorrect e-mail"),
                           DataRequired(message="E-mail is required"),
                       ])
    message = TextAreaField("Message",
                            validators=[
                                Length(max=768),
                                DataRequired(message="Feedback message is required"),
                            ])
    submit = SubmitField("Send")
