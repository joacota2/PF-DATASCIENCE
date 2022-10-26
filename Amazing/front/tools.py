import os
from random import randint
import secrets
from flask import url_for
from flask_login import current_user
from front import db, app
from PIL import Image


def img_placeholder():
    return url_for("static", filename="img_not_available.png")


def get_category(category):
    result = db.session.execute(
        "SELECT Distinct(category),categoryN FROM `pf-henry-365404.SR.reviewLORD` where category is not null order by categoryN"
    )

    for x in result:
        if x[0] == category:
            return x[1]
