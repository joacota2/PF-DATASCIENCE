from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
import requests
from front import bcrypt, db
from threading import Thread

from front.users.forms import (
    UpdateAccountForm,
)
from front.models import Products, Reviews, UsersCart, UsersFavorites, UsersPurchases
from front.store.forms import CheckoutForm

users = Blueprint("users", __name__)


@users.get("/profile")
@login_required
def profile():
    pfp = url_for("static", filename="pfps/" + current_user.pfp)
    reviews = Reviews.query.filter_by(reviewerName=current_user.username).count()
    return render_template("profile.html", title="My profile", pfp=pfp, reviews=reviews)


@users.get("/profile/reviews")
@login_required
def reviews():
    page = request.args.get("page", 1, type=int)
    reviews = (
        Reviews.query.filter_by(reviewerName=current_user.username)
        .order_by(Reviews.Date.desc())
        .order_by(Reviews.unixReviewTime.desc())
        .paginate(page=page, per_page=5)
    )

    return render_template("my_reviews.html", title="My reviews", reviews=reviews)


@users.get("/favorites")
@login_required
def favorites():
    page = request.args.get("page", 1, type=int)
    favorites = UsersFavorites.query.filter_by(user_id=current_user.id).paginate(
        page=page, per_page=5
    )
    return render_template(
        "my_favorites.html", title="My favorites", favorites=favorites
    )


@users.get("/cart")
@login_required
def cart():
    return render_template("my_cart.html", title="My cart")


@users.route("/cart/checkout", methods=["GET", "POST"])
def cart_checkout():
    form = CheckoutForm()
    if request.method == "POST":
        session["data"] = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
        }
        return redirect(url_for("main.loading", destination=f"cart/checkout/success"))
    return render_template("cart_checkout.html", form=form)


@users.get("/cart/checkout/success")
@login_required
def cart_checkout_success():
    if "data" in session:
        data = session["data"]
        current_user.send_purchase_email(data, mode="cart")
        for product in current_user.cart:
            purchase = UsersPurchases(
                user_id=current_user.id, asin=product.product.asin
            )
            db.session.add(purchase)
        db.session.commit()
        return render_template(
            "cart_checkout_success.html", title="Thank you", data=data
        )
    return redirect(url_for("main.home"))


# @users.get("/profile/posts")
# @login_required
# def posts():
#     page = request.args.get("page", 1, type=int)
#     posts = Products.query.filter_by(user_id=current_user.id).paginate(
#         page=page, per_page=5
#     )
#     return render_template("my_posts.html", title="My posts", posts=posts)


@users.route("/profile/update", methods=["POST", "GET"])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.pfp.data:
            current_user.set_pfp(form.pfp.data)
        if form.username.data:
            current_user.set_username(form.username.data)
        if form.email.data:
            current_user.set_email(form.email.data)
        if not form.pfp.data and not form.username.data and not form.email.data:
            flash("At least one field is required.", "error")
        else:
            db.session.commit()
            Thread(target=requests.post, args="/update_user").start()
            flash("Profile updated.", "success")
            return redirect(url_for("main.loading", destination="profile"))

    return render_template("update_account.html", title="Update account", form=form)


@users.route("/update_user", methods=["POST"])
@login_required
def update_reviews():
    for review in current_user.reviews:
        review.reviewerName = current_user.username

    db.session.commit()
