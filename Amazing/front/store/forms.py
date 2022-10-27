from datetime import datetime
from email.policy import default
from flask_login import current_user
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    DataRequired,
)
from flask_wtf import FlaskForm


class CheckoutForm(FlaskForm):
    # Billing data
    first_name = StringField(
        "First name",
        validators=[DataRequired(message="You must provide a first name.")],
    )
    last_name = StringField(
        "Last name",
        validators=[DataRequired(message="You must provide a last name.")],
    )
    email = StringField("Email")
    street = StringField(
        "Street",
        default="Fake Street",
    )
    address = IntegerField(
        "Address",
        default=123,
    )
    address2 = StringField("Indications (Optional)", default="House")
    country = SelectField(
        "Country",
        choices=["Brazil"],
    )
    state_city = StringField(
        "State/City",
        default="Río de Janeiro",
    )
    zip_code = StringField(
        "Zip code",
        default="23900-000",
    )
    # Credit card data
    full_name = StringField(
        "Name on the card",
        default="Homer Simpson",
    )
    card_number = StringField(
        "Credit card number",
        default="6011 0009 9013 9424",
    )
    expiration = StringField("Expiration date", default="06/2058")

    cvv = StringField(
        "CVV",
        default="666",
    )

    submit = SubmitField("Checkout")
