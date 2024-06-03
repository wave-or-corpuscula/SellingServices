from datetime import date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from app.config import Config


db = SQLAlchemy()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.jinja_env.filters['zip'] = zip

    @app.template_filter()
    def kravchuk_date_format(date_value: date):
        return date_value.strftime("%d.%m.%Y")

    db.init_app(app)
    
    from app.users.routes import users
    from app.clients.routs import clients
    from app.employees.routs import employees
    from app.admin.routs import admin
    app.register_blueprint(users)
    app.register_blueprint(clients)
    app.register_blueprint(employees)
    app.register_blueprint(admin)

    return app
