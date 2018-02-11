from flask.ext.sqlalchemy import SQLAlchemy
from pyriver.db.database import DB


db = SQLAlchemy()


def initdb():
    db.Model.metadata.create_all(self.engine)
