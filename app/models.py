from .database import db
from datetime import datetime

class Carteirinha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    foto = db.Column(db.String(200), nullable=False)
    oab_numero = db.Column(db.String(60), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
