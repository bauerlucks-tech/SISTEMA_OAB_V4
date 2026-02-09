from flask import Blueprint, render_template, request, redirect
from .models import Carteirinha
from .database import db
from .services import gerar_carteirinha

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/gerar", methods=["GET", "POST"])
def gerar():
    if request.method == "POST":
        nome = request.form["nome"]
        oab = request.form["oab"]
        foto = request.files["foto"]
        gerar_carteirinha(nome, oab, foto)
        return redirect("/historico")
    return render_template("gerar.html")

@main.route("/historico")
def historico():
    cards = Carteirinha.query.order_by(Carteirinha.data.desc()).all()
    return render_template("historico.html", cards=cards)
