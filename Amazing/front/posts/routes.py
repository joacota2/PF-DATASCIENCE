import secrets
from webbrowser import get
from flask import Blueprint, flash, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required
from front import db
from front.models import (
    Products,
    Reviews,
    UsersCart,
    UsersFavorites,
    UsersHelpful,
    UsersNotHelpful,
)
from front.posts.forms import PostForm
import pyimgur
from front import app
from PIL import Image
import os

posts = Blueprint("posts", __name__)


def get_image_url(img):

    random_hex = secrets.token_hex(8)
    f_ext = ".jpg"
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static", picture_fn)

    img.save(picture_path)

    CLIENT_ID = "66e3dd6c3b2197b"
    im = pyimgur.Imgur(CLIENT_ID)
    image = im.upload_image(picture_path, title="Any")

    os.remove(picture_path.replace(list("\\")[0], "/"))

    return image.link_large_thumbnail


@posts.route("/vote_helpful/<path:review_id>", methods=["POST"])
def like_review(review_id):
    review = Reviews.query.filter_by(id=review_id).first()
    vote = UsersHelpful.query.filter_by(
        review=review.id, user_id=current_user.id
    ).first()

    if not review.helpful:
        review.helpful = str([0, 0])

    if not review:
        return jsonify({"error": "Review not found."}, 400)
    elif vote:
        db.session.delete(vote)
        db.session.commit()
    else:
        vote = UsersHelpful(user_id=current_user.id, review=review_id)
        db.session.add(vote)
        db.session.commit()

    return jsonify(
        {
            "votes": len(review.helpful_users) + eval(review.helpful)[0],
            "voted": current_user.id in map(lambda x: x.user_id, review.helpful_users),
        }
    )


@posts.route("/vote_unhelpful/<path:review_id>", methods=["POST"])
def dislike_review(review_id):
    review = Reviews.query.filter_by(id=review_id).first()
    vote = UsersNotHelpful.query.filter_by(
        review=review.id, user_id=current_user.id
    ).first()

    if not review.helpful:
        review.helpful = str([0, 0])

    if not review:
        return jsonify({"error": "Review not found."}, 400)
    elif vote:
        db.session.delete(vote)
        db.session.commit()
    else:
        vote = UsersNotHelpful(user_id=current_user.id, review=review_id)
        db.session.add(vote)
        db.session.commit()

    return jsonify(
        {
            "votes": len(review.not_helpful_users) + eval(review.helpful)[0],
            "voted": current_user.id
            in map(lambda x: x.user_id, review.not_helpful_users),
        }
    )


@posts.route("/add2favs/<path:asin>", methods=["POST"])
def favorite(asin):
    product = Products.query.filter_by(asin=asin).first()
    favorite = UsersFavorites.query.filter_by(asin=asin).first()

    if not product:
        return jsonify({"error": "Product not found."}, 400)
    elif favorite:
        db.session.delete(favorite)
        db.session.commit()
        print(f"Removed from favs: {asin}")
    else:
        favorite = UsersFavorites(user_id=current_user.id, asin=asin)
        db.session.add(favorite)
        db.session.commit()
        print(f"Added to favs: {asin}")
    return jsonify(
        {
            "in_favs": favorite.id in map(lambda x: x.id, current_user.favorites),
        }
    )


@posts.route("/add2cart/<path:asin>", methods=["POST"])
def cart(asin):
    product = Products.query.filter_by(asin=asin).first()
    cart_item = UsersCart.query.filter_by(asin=asin).first()

    if not product:
        return jsonify({"error": "Product not found."}, 400)
    elif cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        print(f"Removed from cart: {asin}")
    else:
        cart_item = UsersCart(user_id=current_user.id, asin=asin)
        db.session.add(cart_item)
        db.session.commit()
        print(f"Added to cart: {asin}")

    return jsonify(
        {
            "in_cart": cart_item.id in map(lambda x: x.id, current_user.cart),
        }
    )


@posts.route("/posts/new", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():

        if current_user.is_authenticated:

            if not form.image.data:
                flash("You must provide an image for your product.", "danger")

                redirect(url_for("posts.new_post"))

            post = Products(
                price=form.price.data,
                description=form.description.data,
                brand=form.brand.data,
                category=form.category.data,
                title=form.title.data,
                image=get_image_url(form.image.data),
            )

            db.session.add(post)
            db.session.commit()

            flash("Product posted successfully.", "success")

            return render_template("loading.html", destination=f"product/{post.asin}")

        return render_template("loading.html", destination="login")

    return render_template("new_post.html", form=form)
