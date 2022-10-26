from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint("main", __name__)


@main.get("/loading/<path:destination>")
def loading(destination):
    return render_template("loading.html", destination=destination)


# TODO
@main.get("/")
@main.get("/home")
def home():
    return render_template("home.html")


@main.get("/about")
def about():
    return render_template("about.html")
