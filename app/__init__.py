from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()


def create_app(config=Config):
    app = Flask(__name__)
    app.config["SECRET_KEY"]="sjdFODJdsojfsodfjPFJdjs546sdfsoidfjPfj"
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///program.sqlite"
    # app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Db created!")

    return app
