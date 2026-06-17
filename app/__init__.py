from flask import Flask
from flask_wtf import CSRFProtect

from config import Config

from .models import db

csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config["REPORT_DIR"].mkdir(exist_ok=True)
    app.instance_path

    db.init_app(app)
    csrf.init_app(app)

    from .routes import main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
