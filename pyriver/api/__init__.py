from flask import Flask

from server.routes import bp as root_bp
from server.db import db
import settings


def create_app():
    app = Flask(
        __name__,
        static_folder=settings.STATIC_FOLDER,
        template_folder=settings.TEMPLATE_FOLDER
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.register_blueprint(root_bp)
    return app
