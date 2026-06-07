from flask import Flask
from app.models import init_db
from app.routes import dashboard, laptop, employee


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db(app)

    from app.routes import dashboard
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(laptop.bp)
    app.register_blueprint(employee.bp)

    return app