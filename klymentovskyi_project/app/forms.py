from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


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
