from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    DataRequired,
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from front import real_categories, db_categories


class ReviewForm(FlaskForm):
    summary = StringField(
        "Title of the review",
        validators=[InputRequired(message="You must provide a title.")],
    )
    content = TextAreaField(
        "Write your review here",
        validators=[
            InputRequired(message="You must provide a content."),
            Length(max=2000),
        ],
    )
    overall = SelectField(
        "Overall", choices=[(5, "★ 5"), (4, "★ 4"), (3, "★ 3"), (2, "★ 2"), (1, "★ 1")]
    )
    submit = SubmitField("Post")


class PostForm(FlaskForm):
    title = StringField(
        "Title of the post",
        validators=[InputRequired(message="You must provide a title.")],
    )
    description = TextAreaField(
        "Description of the post",
        validators=[InputRequired(message="You must provide a description")],
    )
    price = DecimalField(
        "Price of the product",
        validators=[InputRequired("Please provide a price for this product.")],
    )
    brand = StringField(
        "Brand of the product",
        validators=[InputRequired("You must provide a brand for you product.")],
    )
    category = SelectField(
        "Category",
        choices=[
            (cat, real_cat) for cat, real_cat in zip(db_categories, real_categories)
        ],
    )
    image = FileField(
        "Image of the product",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"]),
        ],
    )
    submit = SubmitField("Post")
