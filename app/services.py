
import os, uuid
from psd_tools import PSDImage
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import current_app
from .models import Carteirinha, Configuracao
from .database import db

def obter_proximo_registro():
    cfg = Configuracao.query.first()
    if not cfg:
        cfg = Configuracao(proximo_registro=1)
        db.session.add(cfg)
        db.session.commit()
    numero = cfg.proximo_registro
    cfg.proximo_registro += 1
    db.session.commit()
    return numero

def gerar_png_do_psd(psd_path, dados, foto_path=None):
    psd = PSDImage.open(psd_path)
    imagem = psd.compose()

    if foto_path:
        foto = Image.open(foto_path).convert("RGBA")
        foto = foto.resize((300, 400))
        imagem.paste(foto, (50, 50))

    draw = ImageDraw.Draw(imagem)
    for chave, valor in dados.items():
        draw.text((50, 500), f"{chave}: {valor}", fill=(0,0,0))

    nome = str(uuid.uuid4()) + ".png"
    destino = os.path.join(current_app.config["OUTPUT_FOLDER"], nome)
    imagem.save(destino)
    return destino

def gerar_pdf(frente, verso):
    nome = frente.replace(".png", ".pdf")
    c = canvas.Canvas(nome, pagesize=A4)
    c.drawImage(frente, 50, 400, width=500, height=300)
    c.drawImage(verso, 50, 50, width=500, height=300)
    c.save()
    return nome

def processar_carteirinha(form, foto):
    registro = obter_proximo_registro()

    dados = {
        "NOME": form.get("nome"),
        "RG": form.get("rg"),
        "CPF": form.get("cpf"),
        "TELEFONE": form.get("telefone"),
        "NASCIMENTO": form.get("nascimento"),
        "REGISTRO": registro,
        "CIDADE": "São Paulo"
    }

    foto_nome = None
    if foto:
        foto_nome = os.path.join(current_app.config["UPLOAD_FOLDER"], foto.filename)
        foto.save(foto_nome)

    frente = gerar_png_do_psd(
        os.path.join(current_app.config["PSD_FOLDER"], "Frente.psd"),
        dados,
        foto_nome
    )

    verso = gerar_png_do_psd(
        os.path.join(current_app.config["PSD_FOLDER"], "Verso.psd"),
        dados
    )

    pdf = gerar_pdf(frente, verso)

    card = Carteirinha(
        nome=form.get("nome"),
        oab=str(registro),
        arquivo_png_frente=frente,
        arquivo_png_verso=verso,
        arquivo_pdf=pdf
    )

    db.session.add(card)
    db.session.commit()
