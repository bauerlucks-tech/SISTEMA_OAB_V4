import os
import uuid
from flask import current_app

def salvar_foto(foto):
    nome_unico = str(uuid.uuid4()) + "_" + foto.filename
    destino = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_unico)
    foto.save(destino)
    return nome_unico
