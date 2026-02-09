
from flask import Blueprint, render_template, request, redirect
from .services import processar_carteirinha
from .models import Carteirinha

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/gerar", methods=["GET", "POST"])
def gerar():
    if request.method == "POST":
        processar_carteirinha(request.form, request.files.get("foto"))
        return redirect("/historico")
    return render_template("gerar.html")

@main.route("/historico")
def historico():
    cards = Carteirinha.query.all()
    return render_template("historico.html", cards=cards)
