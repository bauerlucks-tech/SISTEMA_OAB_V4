
from flask import Flask
from .config import Config
from .database import db

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app
