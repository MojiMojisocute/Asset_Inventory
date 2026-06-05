from flask import Flask
from app.models import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db(app)

    from app.routes import dashboard
    app.register_blueprint(dashboard.bp)

    return app