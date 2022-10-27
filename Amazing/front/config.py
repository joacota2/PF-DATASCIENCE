import os


class Config:
    SECRET_KEY = "d9fd5491c527534ad96583b276318abebc55bbbfaac459554d3a69b4e756871f"
    SQLALCHEMY_DATABASE_URI = "bigquery://pf-henry-365404/SR"
    # SECRET_KEY = os.environ["SECRET_KEY"]
    # SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
