import os
from .models import Carteirinha
from .database import db
from .utils import salvar_foto

def gerar_carteirinha(nome, oab, foto):
    caminho = salvar_foto(foto)
    card = Carteirinha(nome=nome, oab_numero=oab, foto=caminho)
    db.session.add(card)
    db.session.commit()
