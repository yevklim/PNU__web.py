from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField("Username", id="username", name="username",
                           validators=[
                               DataRequired(message="Username is required"),
                           ])
    password = PasswordField("Password", id="password", name="password",
                             validators=[
                                 DataRequired("Password is required"),
                                 Length(min=4, max=32)
                             ])
    remember_me = BooleanField("Remember Me", id="remember-me", name="remember-me",
                               validators=[
                               ])
    submit = SubmitField("Sign In")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", id="current-password", name="current-password",
                                     validators=[
                                         DataRequired("Required"),
                                         Length(min=4, max=32)
                                     ])
    new_password = PasswordField("New Password", id="new-password", name="new-password",
                                 validators=[
                                     DataRequired("Required"),
                                     Length(min=4, max=32),
                                     EqualTo("confirm_password", "Passwords must match")
                                 ])
    confirm_password = PasswordField("Confirm Password", id="confirm-password", name="confirm-password",
                                     validators=[
                                         DataRequired("Required"),
                                         Length(min=4, max=32),
                                         EqualTo("new_password", "Passwords must match")
                                     ])
    submit = SubmitField("Change")

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
