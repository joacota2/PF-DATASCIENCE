from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from front.models import Users
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from flask_wtf import FlaskForm


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            Length(min=4, message="Username must be at least 4 characters long.")
        ],
    )
    email = StringField(
        "Email", validators=[Email(message="Must be a valid email address.")]
    )

    pfp = FileField("Profile picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit = SubmitField("Update profile")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already registered.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already registered.")
