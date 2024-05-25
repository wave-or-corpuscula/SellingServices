from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    
    from app.users.routes import users
    from app.clients.routs import clients
    from app.employees.routs import employees
    app.register_blueprint(users)
    app.register_blueprint(clients)
    app.register_blueprint(employees)

    return app
