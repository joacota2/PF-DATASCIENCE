from sqlalchemy.engine import create_engine
import flask_sqlalchemy.
import flask_sqlalchemy
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials.json"

engine = create_engine("bigquery://pf-henry-365404")
meta = flask_sqlalchemy.MetaData(bind=engine)
table = flask_sqlalchemy.schema.Table("SR.metaLORD", meta, autoload=True)
print(engine.execute(flask_sqlalchemy.select(table).limit(1)).all())
