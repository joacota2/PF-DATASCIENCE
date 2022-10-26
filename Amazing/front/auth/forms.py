from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from front.models import Users
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            InputRequired("Please choose a username."),
            Length(min=4, message="Username must be at least 4 characters long."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired("Please choose an email."),
            Email("Must be a valid email address.", check_deliverability=True),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired("Please choose a password."),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            InputRequired("Please confirm your password."),
            Length(min=8, message="Password must be at least 8 characters long."),
            EqualTo("password", message="Passwords must be the same."),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already registered.")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            InputRequired("You must introduce an email account."),
            Email("Must be a valid email address."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired("You must introduce a password."),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RequestPasswordResetForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            InputRequired("You must introduce an email account."),
            Email(message="Must be a valid email address."),
        ],
    )
    submit = SubmitField("Send request")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Theres no user registered with this email address.")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        "New password", validators=[InputRequired("You must enter a new password")]
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[InputRequired("Must be equal to the new password")],
    )
    submit = SubmitField("Reset password")
