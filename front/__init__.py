from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from front.config import Config
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "front/credentials.json"


def listify(value):
    return eval(value)


def overall_stars(overall):
    return "★".zfill(int(overall)).replace("0", "★")


def get_max(items):
    item_list = [x for x in items if x != None]
    return max(item_list)


app = Flask(__name__)


with app.app_context():
    app.config.from_object(Config)

    app.jinja_env.globals.update(listify=listify)
    app.jinja_env.globals.update(int=int)
    app.jinja_env.globals.update(str=str)
    app.jinja_env.globals.update(get_max=get_max)
    app.jinja_env.globals.update(overall_stars=overall_stars)
    app.jinja_env.globals.update(round=round)
    app.jinja_env.globals.update(sum=sum)

    db = SQLAlchemy(app)

    bcrypt = Bcrypt(app)

    mail = Mail(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from front.models import *

    db.create_all()

    db_categories = (
        db.session.query(Products.category)
        .where(Products.category != None)
        .order_by(Products.category.asc())
        .distinct()
        .all()
    )

    real_categories = [
        category.category.replace("amp;", "")
        .lower()
        .replace(" ", "_")
        .title()
        .replace("_", " ")
        for category in db_categories
    ]

    app.jinja_env.globals.update(Products=Products)
    app.jinja_env.globals.update(db_categories=db_categories)
    app.jinja_env.globals.update(real_categories=real_categories)

    from front.users.routes import users
    from front.main.routes import main
    from front.store.routes import store
    from front.posts.routes import posts
    from front.auth.routes import auth

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(store)
    app.register_blueprint(posts)
    app.register_blueprint(auth)
