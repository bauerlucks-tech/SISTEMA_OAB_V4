from flask import Flask
from .config import Config
from .database import db


def create_app():
    app = Flask(__name__)

    # Configurações
    app.config.from_object(Config)

    # Banco de dados
    db.init_app(app)

    # Importa e registra rotas
    from .routes import main
    app.register_blueprint(main)

    # Cria tabelas (se necessário)
    with app.app_context():
        db.create_all()

    return app
