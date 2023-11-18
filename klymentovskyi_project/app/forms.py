from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp, ValidationError
from app import models
from flask_login import current_user


class LoginForm(FlaskForm):
    email = EmailField("E-mail",
                        validators=[
                            Length(max=120),
                            Email(message="Incorrect e-mail"),
                            DataRequired(message="E-mail is required"),
                        ])
    password = PasswordField("Password", id="password", name="password",
                             validators=[
                                 DataRequired("Password is required"),
                                 Length(min=6, max=60)
                             ])
    remember_me = BooleanField("Remember Me", id="remember-me", name="remember-me",
                               validators=[
                               ])
    submit = SubmitField("Sign In")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(message="Username is required"),
                               Length(min=4, max=20),
                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                      'Username must have only '
                                      'letters, numbers, dots '
                                      'or underscores'),
                           ])
    email = EmailField("E-mail",
                        validators=[
                            Length(max=120),
                            Email(message="Incorrect e-mail"),
                            DataRequired(message="E-mail is required"),
                        ])
    picture = FileField("Update Profile Picture",
                       validators=[
                           FileAllowed(["jpg", "png"])
                       ])
    about_me = TextAreaField("About Me",
                             validators=[
                                 Length(max=512),
                             ])
    submit = SubmitField("Update")

    def validate_email(self, field):
        if field.data == current_user.email:
            return

        if models.User.query.filter_by(email=field.data).first():
            raise ValidationError("E-mail already registered.")

    def validate_username(self, field):
        if field.data == current_user.username:
            return

        if models.User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", id="current-password", name="current-password",
                                     validators=[
                                         DataRequired("Required"),
                                         Length(min=6, max=60)
                                     ])
    new_password = PasswordField("New Password", id="new-password", name="new-password",
                                 validators=[
                                     DataRequired("Required"),
                                     Length(min=6, max=60),
                                     EqualTo("confirm_password", "Passwords must match")
                                 ])
    confirm_password = PasswordField("Confirm Password", id="confirm-password", name="confirm-password",
                                     validators=[
                                         DataRequired("Required"),
                                         Length(min=6, max=60),
                                         EqualTo("new_password", "Passwords must match")
                                     ])
    submit = SubmitField("Change")

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError("Incorrect current password.")

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(message="Username is required"),
                               Length(min=4, max=20),
                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                      'Username must have only '
                                      'letters, numbers, dots '
                                      'or underscores'),
                           ])
    email = EmailField("E-mail",
                        validators=[
                            Length(max=120),
                            Email(message="Incorrect e-mail"),
                            DataRequired(message="E-mail is required"),
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired("Password is required"),
                                 Length(min=6, max=60),
                                 EqualTo("confirm_password", "Passwords must match"),
                             ])
    confirm_password = PasswordField("Confirm Password", id="confirm-password", name="confirm-password",
                                     validators=[
                                         DataRequired("Required"),
                                         Length(min=6, max=60),
                                         EqualTo("password", "Passwords must match"),
                                     ])
    submit = SubmitField("Sign Up")

    def validate_email(self, field):
        if models.User.query.filter_by(email=field.data).first():
            raise ValidationError("E-mail already registered.")

    def validate_username(self, field):
        if models.User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")

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
