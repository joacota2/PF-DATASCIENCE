from random import randint
from flask import Blueprint, render_template
from flask_login import current_user

from front.models import UsersRecommendations
from front import db

main = Blueprint("main", __name__)


@main.get("/loading/<path:destination>")
def loading(destination):
    return render_template("loading.html", destination=destination)


# TODO
@main.get("/")
@main.get("/home")
def home():
    max_recom = 8
    recommendations = (
        UsersRecommendations.query.offset(
            randint(1, UsersRecommendations.query.count() - max_recom)
        )
        .limit(max_recom)
        .all()
    )
    for rec in recommendations:
        rec.product.title = rec.product.title.replace("amp;", "")
    db.session.commit()
    return render_template("home.html", recommendations=recommendations)


@main.get("/about")
def about():
    return render_template("about.html")
