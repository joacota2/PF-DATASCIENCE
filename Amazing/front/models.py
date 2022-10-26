from email.mime.text import MIMEText
import os
from random import randint
import secrets
import smtplib
import ssl
import time
from flask import url_for
from itsdangerous import TimedSerializer
from front import db, login_manager, app, bcrypt
from flask_login import UserMixin, current_user
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from PIL import Image


def gen_id():
    return secrets.token_hex(50)


def gen_token():
    token = secrets.token_hex(100)
    user = Users.query.filter_by(activation_token=token).first()
    if user:
        gen_token()
    return token


def get_unix():
    return int(time.time())


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    creation_date = db.Column(db.DateTime, default=datetime.today)
    username = db.Column(db.Text, unique=True, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=True)
    pfp = db.Column(db.Text, default="default_pfp.jpg")
    password = db.Column(db.Text, nullable=True)
    is_activated = db.Column(db.Boolean, default=False)
    activation_token = db.Column(db.String(255), default=gen_token)
    is_admin = db.Column(db.Boolean, default=False)
    favorites = db.relationship("UsersFavorites", backref="user", passive_deletes=True)
    reviews = db.relationship(
        "Reviews",
        backref="user",
        passive_deletes=True,
    )
    helpful_reviews = db.relationship(
        "UsersHelpful", backref="user", passive_deletes=True
    )
    not_helpful_reviews = db.relationship(
        "UsersNotHelpful", backref="user", passive_deletes=True
    )
    cart = db.relationship("UsersCart", backref="user", passive_deletes=True)
    purchases = db.relationship("UsersPurchases", backref="user", passive_deletes=True)
    discounts = db.relationship("UsersDiscounts", backref="user", passive_deletes=True)

    def get_reset_token(self):
        s = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        try:
            user_id = s.loads(token, max_age=max_age)["user_id"]
        except:
            return None
        return Users.query.get(user_id)

    def send_reset_email(self):

        sender = "amazingstoreactivation@gmail.com"

        pwd = "naczaucjjhpnrxkf"

        receiver = self.email

        subject = "Password reset request."

        body = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <h1>A password reset has been requested. If it wasn't you, please ignore this.</h1>

    <a href="{}">Reset your password.</a>
</body>

</html>
""".format(
            url_for("auth.reset_password", token=self.get_reset_token(), _external=True)
        )

        email = MIMEMultipart()
        email["from"] = sender
        email["to"] = receiver
        email["Subject"] = subject
        email.attach(MIMEText(body, "html"))

        ctx = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
            smtp.login(user=sender, password=pwd)
            smtp.sendmail(sender, receiver, email.as_string())

    def send_purchase_email(self, data, mode, product=None):
        sender = "amazingstoreactivation@gmail.com"

        pwd = "naczaucjjhpnrxkf"

        receiver = self.email

        if mode == "single" or mode == 0:

            subject = f"Thank you for your purchase: {product.title}"

            total = int(product.price) - 5

            if total <= 3:
                total = 3

            body = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <h2>Order: {product.title} x1</h2>

    <h4>Here in AmazingStore it's all about you, {data['first_name']}. We hope you had a good experience :)</h4>
    
    <h3>Summary:</h3>
    
    <table>
        <thead>
            <tr>
                <th>Product</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            <td>
                { product.title }</td>
            <td>${ int(product.price) }</td>
        </tbody>
        <tbody>
            <td><strong>AMAZINGSTORE</strong></td>
            <td><strong>-$5</strong></td>
        </tbody>
        <tbody>
            <td><strong>ESTIMATED TOTAL</strong></td>
            <td><strong>${total}</strong></td>
        </tbody>
    </table>  
    <small style="color:#b5b5b5">None of this is true. This email it's for immersing purposes only.</small>
</body>

</html>
"""

        elif mode == "cart" or mode == 1:

            subject = f"Thank you for your purchase."

            total = sum([cart_item.product.price for cart_item in self.cart])

            rows = [
                f"""<tbody>
    <td>
        { cart_item.product.title }</td>
    <td>${ int(cart_item.product.price) }</td>
</tbody>"""
                for cart_item in self.cart
            ]

            body = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <h2>Order: {len(self.cart)} products</h2>

    <h4>Here in AmazingStore it's all about you, {data['first_name']}. We hope you had a good experience :)</h4>
    
    <h3>Summary:</h3>
    
    <table>
        <thead>
            <tr>
                <th>Product</th>
                <th>Price</th>
            </tr>
        </thead>
        {''.join(rows)}
        <tbody>
            <td><strong>AMAZINGSTORE</strong></td>
            <td><strong>-$5</strong></td>
        </tbody>
        <tbody>
            <td><strong>ESTIMATED TOTAL</strong></td>
            <td><strong>${total}</strong></td>
        </tbody>
    </table>  
    <small style="color:#b5b5b5">None of this is true. This email it's for immersing purposes only.</small>
</body>

</html>
"""

        email = MIMEMultipart()
        email["from"] = sender
        email["to"] = receiver
        email["Subject"] = subject
        email.attach(MIMEText(body, "html"))

        ctx = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
            smtp.login(user=sender, password=pwd)
            smtp.sendmail(sender, receiver, email.as_string())

    def set_password(self, password):
        new_hashed_pwd = bcrypt.generate_password_hash(password).decode("utf-8")
        self.password = new_hashed_pwd

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def set_pfp(self, form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        if "default_pfp.jpg" not in current_user.pfp:
            old_path = os.path.join(app.root_path, "static\pfps", current_user.pfp)
            os.remove(old_path.replace(list("\\")[0], "/"))
        picture_path = os.path.join(app.root_path, "static/pfps", picture_fn)
        output_size = (250, 250)
        i = Image.open(form_picture)
        i.thumbnail(output_size, Image.ANTIALIAS)
        i.save(picture_path)
        self.pfp = picture_fn
        return picture_fn

    def get_reviews(self):
        return self.reviews.query.filter_by(reviewerID=self.id)


class Products(db.Model):
    __tablename__ = "metaLORD"
    asin = db.Column(db.Text, primary_key=True, default=gen_id)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    index = db.Column(db.Integer, nullable=True)
    brand = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    bought_together = db.Column(db.Text, nullable=True)
    buy_after_viewing = db.Column(db.Text, nullable=True)
    imUrl = db.Column(db.Text, nullable=True)
    also_bought = db.Column(db.Text, nullable=True)
    also_viewed = db.Column(db.Text, nullable=True)
    categories = db.Column(db.Text, nullable=True)
    salesRank = db.Column(db.Text, nullable=True)
    reviews = db.relationship("Reviews", backref="product", passive_deletes=True)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    purchases = db.relationship(
        "UsersPurchases", backref="product", passive_deletes=True
    )
    discounts = db.relationship(
        "UsersDiscounts", backref="product", passive_deletes=True
    )
    favorites = db.relationship(
        "UsersFavorites", backref="product", passive_deletes=True
    )
    carts = db.relationship("UsersCart", backref="product", passive_deletes=True)


class Reviews(db.Model):
    __tablename__ = "reviewLORD_reborn"
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    reviewerID = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    asin = db.Column(
        db.Text, db.ForeignKey("metaLORD.asin", ondelete="CASCADE"), nullable=False
    )
    reviewerName = db.Column(db.Text, nullable=True)
    helpful = db.Column(db.Text, default=str([0, 0]))
    reviewText = db.Column(db.Text, nullable=False)
    overall = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    unixReviewTime = db.Column(db.Integer, default=get_unix)
    Date = db.Column(db.Date, default=datetime.today)
    category = db.Column(db.Text, nullable=False)
    categoryN = db.Column(db.Integer, nullable=True)
    helpful_users = db.relationship(
        "UsersHelpful", backref="helpful_review", passive_deletes=True
    )
    not_helpful_users = db.relationship(
        "UsersNotHelpful", backref="not_helpful_review", passive_deletes=True
    )


class UsersHelpful(db.Model):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    review = db.Column(
        db.Text,
        db.ForeignKey("reviewLORD_reborn.id", ondelete="CASCADE"),
        nullable=False,
    )


class UsersNotHelpful(db.Model):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    review = db.Column(
        db.Text,
        db.ForeignKey("reviewLORD_reborn.id", ondelete="CASCADE"),
        nullable=False,
    )


class UsersFavorites(db.Model):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    date_created = db.Column(db.Date, default=datetime.today)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    asin = db.Column(
        db.Text, db.ForeignKey("metaLORD.asin", ondelete="CASCADE"), nullable=False
    )


class UsersCart(db.Model):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    asin = db.Column(
        db.Text, db.ForeignKey("metaLORD.asin", ondelete="CASCADE"), nullable=False
    )


class UsersPurchases(db.Model):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    date_bought = db.Column(db.Date, default=datetime.today)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    asin = db.Column(
        db.Text, db.ForeignKey("metaLORD.asin", ondelete="CASCADE"), nullable=False
    )


class UsersDiscounts(db.Model):
    id = db.Column(db.Text, primary_key=True, default=gen_id)
    user_id = db.Column(
        db.Text, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    asin = db.Column(
        db.Text, db.ForeignKey("metaLORD.asin", ondelete="CASCADE"), nullable=False
    )
    discount = db.Column(db.Integer, default=randint(3, 18))


# ! TODO RECOMMENDATIONS
