
from .database import db
from datetime import datetime

class Configuracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proximo_registro = db.Column(db.Integer, default=1)

class Carteirinha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    oab = db.Column(db.String(60))
    arquivo_png_frente = db.Column(db.String(200))
    arquivo_png_verso = db.Column(db.String(200))
    arquivo_pdf = db.Column(db.String(200))
    data = db.Column(db.DateTime, default=datetime.utcnow)
