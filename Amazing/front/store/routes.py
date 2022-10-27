from datetime import date
from random import randint
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from front.posts.forms import ReviewForm
from front import db

from front.models import Products, Reviews, UsersDiscounts, UsersPurchases
from front.tools import get_category, img_placeholder
from front.store.forms import CheckoutForm

store = Blueprint("store", __name__)


@store.get("/catalog")
def catalog():
    page = request.args.get("page", 1, type=int)
    products = (
        Products.query.filter(
            db.and_(
                Products.category != "N/A",
                Products.category != None,
                Products.title != "N/A",
            ),
        )
        .order_by(Products.salesRank.desc())
        .paginate(page=page, per_page=12)
    )
    for prod in products.items:
        prod.title = prod.title.replace("amp;", "")
        prod.category = prod.category.replace("amp;", "")
    db.session.commit()
    return render_template(
        "catalog.html",
        title="Catalog",
        products=products,
        img_placeholder=img_placeholder(),
        page=page,
    )


@store.route("/product/<path:asin>", methods=["POST", "GET"])
def product(asin):

    form = ReviewForm()

    product = Products.query.filter_by(
        asin=asin,
    ).first()

    if form.validate_on_submit():

        if current_user.is_authenticated:

            review = Reviews(
                reviewerID=current_user.id,
                asin=asin,
                reviewerName=current_user.username,
                helpful=str([0, 0]),
                reviewText=form.content.data,
                overall=form.overall.data,
                summary=form.summary.data,
                Date=date.today(),
                categoryN=get_category(product.category),
                category=product.category,
            )

            db.session.add(review)
            db.session.commit()

            flash("Review posted successfully.", "success")

            return render_template("loading.html", destination=f"product/{asin}")

        return render_template("loading.html", destination="login")

    if (
        product.price == "N/A"
        or product.price == 0.0
        or len(str(product.price).split(".")[1]) > 2
        or product.price < 5
    ):
        product.price = int(randint(5, 1200))
        db.session.commit()

    texts = ["amp;", "&quot;", "[", "]"]

    for t in texts:
        product.title = product.title.replace(t, "")

    if product.also_bought != "N/A":
        temp_asin = eval(product.also_bought)

        if product.also_bought.count("'") == 2:
            also_bought = (
                Products.query.filter(
                    db.and_(
                        db.or_(Products.asin == x for x in temp_asin),
                        db.and_(
                            Products.category != "N/A",
                            Products.category != None,
                            Products.title != "N/A",
                        ),
                    )
                )
                .order_by(Products.salesRank.desc())
                .limit(3)
                .all()
            )
        else:
            also_bought = (
                Products.query.filter(
                    db.and_(
                        db.or_(Products.asin == x for x in temp_asin),
                        db.and_(
                            Products.category != "N/A",
                            Products.category != None,
                            Products.title != "N/A",
                        ),
                    )
                )
                .order_by(Products.salesRank.desc())
                .limit(3)
                .all()
            )

        for prod in also_bought:
            for t in texts:
                prod.title = prod.title.replace(t, "")

        db.session.commit()
    else:
        also_bought = []

    page = request.args.get("page")

    reviews = (
        Reviews.query.filter(Reviews.asin == product.asin)
        .order_by(Reviews.Date.desc(), Reviews.unixReviewTime.desc())
        .paginate(page=page, per_page=5)
    )

    return render_template(
        "product.html",
        title=product.title,
        product=product,
        also_bought=also_bought,
        reviews=reviews,
        form=form,
    )


@store.route("/product/<path:asin>/checkout", methods=["GET", "POST"])
@login_required
def single_checkout(asin):
    form = CheckoutForm()
    product = Products.query.filter_by(asin=asin).first()
    if request.method == "POST":
        session["data"] = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
        }
        return redirect(
            url_for("main.loading", destination=f"product/{asin}/checkout/success")
        )

    return render_template(
        "single_checkout.html", title="Checkout", product=product, form=form
    )


@store.get("/product/<path:asin>/checkout/success")
@login_required
def single_checkout_success(asin):
    product = Products.query.filter_by(asin=asin).first()
    if "data" in session and product:
        data = session["data"]
        current_user.send_purchase_email(product=product, data=data, mode="single")
        purchase = UsersPurchases(user_id=current_user.id, asin=product.asin)
        db.session.add(purchase)
        db.session.commit()
        return render_template(
            "single_checkout_success.html",
            title="Thank you",
            data=data,
            product=product,
        )
    return redirect(url_for("main.home"))


@store.route("/cart/checkout", methods=["GET", "POST"])
@login_required
def cart_checkout():
    form = CheckoutForm()
    if request.method == "POST":
        return redirect(url_for("main.loading", destination=f"card/checkout/success"))
    return render_template("cart_checkout.html", title="Checkout", form=form)


@store.get("/cart/checkout/success")
@login_required
def cart_checkout_success():
    return render_template("cart_checkout_success.html", title="Thank you")


@store.get("/discounts")
@login_required
def discounts():
    if not current_user.discounts:
        products = (
            Products.query.filter(
                db.and_(
                    Products.category != None,
                    Products.category != "N/A",
                    Products.title != "N/A",
                )
            )
            .order_by(Products.price.desc())
            .offset(randint(1, Products.query.count() - 12))
            .limit(12)
            .all()
        )
        discounts = [
            UsersDiscounts(user_id=current_user.id, asin=prod.asin) for prod in products
        ]
        for d in discounts:
            db.session.add(d)
        db.session.commit()
    elif len(current_user.discounts) < 12:
        current = len(current_user.discounts)
        products = (
            Products.query.filter(
                db.and_(
                    Products.category != None,
                    Products.category != "N/A",
                    Products.title != "N/A",
                )
            )
            .order_by(Products.price.desc())
            .offset(randint(1, 20000))
            .limit(12 - current)
            .all()
        )
        discounts = [
            UsersDiscounts(user_id=current_user.id, asin=prod.asin) for prod in products
        ]
        for d in discounts:
            db.session.add(d)
        db.session.commit()
    discounts = (
        Products.query.filter(
            db.or_(Products.asin == prod.asin for prod in current_user.discounts)
        )
        .order_by(Products.salesRank.desc())
        .all()
    )
    return render_template("discounts.html", title="Discounts", discounts=discounts)


@store.route("/discount/<path:asin>")
def discount(asin):
    if not current_user.is_authenticated:
        flash("Discounts are generated specifically for you. Pleas login first.")
        redirect("auth.login")
    form = ReviewForm()
    if form.validate_on_submit():

        if current_user.is_authenticated:

            review = Reviews(
                reviewerID=current_user.id,
                asin=asin,
                reviewerName=current_user.username,
                helpful=str([0, 0]),
                reviewText=form.content.data,
                overall=form.overall.data,
                summary=form.summary.data,
                Date=date.today(),
                categoryN=get_category(product.category),
                category=product.category,
            )

            db.session.add(review)
            db.session.commit()

            flash("Review posted successfully.", "success")

            return render_template("loading.html", destination=f"product/{asin}")

        return render_template("loading.html", destination="login")

    product = Products.query.filter(Products.asin == asin).first()
    discount = (
        UsersDiscounts.query.filter_by(user_id=current_user.id, asin=asin)
        .first()
        .discount
    )
    page = request.args.get("page")
    reviews = (
        Reviews.query.filter(Reviews.asin == product.asin)
        .order_by(Reviews.Date.desc(), Reviews.unixReviewTime.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "product.html",
        title=product.title,
        form=form,
        product=product,
        discount=discount,
        reviews=reviews,
    )


@store.route("/categories/<path:category>")
def get_category(category):
    page = request.args.get("page")
    products = Products.query.filter(
        db.and_(
            db.and_(
                Products.category != None,
                Products.category != "N/A",
                Products.title != "N/A",
            ),
            db.or_(
                Products.category == category.replace("amp;", ""),
                Products.category == category,
            ),
        )
    ).paginate(page=page, per_page=15)
    return render_template(
        "category.html",
        title=category.replace("amp;", "")
        .lower()
        .replace(" ", "_")
        .title()
        .replace("_", " "),
        real_category=category,
        products=products,
    )
