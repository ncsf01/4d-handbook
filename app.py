import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)


def conectar_bd():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


def censurar_email(email):
    usuario, _, dominio = email.partition("@")
    return f"{usuario[:1]}***@{dominio}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return render_template("about.html")


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        assunto = request.form.get("subject", "").strip()
        mensagem = request.form.get("message", "").strip()

        if not email or "@" not in email or not assunto or not mensagem:
            return redirect(url_for("contato", status="invalido"))

        try:
            conexao = conectar_bd()
            with conexao.cursor() as cursor:
                sql = "INSERT INTO contatos (email, assunto, mensagem) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email[:255], assunto[:150], mensagem))
            conexao.commit()
            conexao.close()
        except pymysql.MySQLError as erro:
            app.logger.error("Erro ao salvar contato: %s", erro)
            return redirect(url_for("contato", status="erro"))

        return redirect(url_for("contato", status="enviado"))

    return render_template("contato.html", status=request.args.get("status"))


@app.route("/mensagens")
def mensagens():
    try:
        conexao = conectar_bd()
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT id, email, assunto, mensagem, criado_em FROM contatos ORDER BY id DESC"
            )
            contatos = cursor.fetchall()
        conexao.close()
    except pymysql.MySQLError as erro:
        app.logger.error("Erro ao listar contatos: %s", erro)
        contatos = None

    if contatos:
        for contato in contatos:
            contato["email"] = censurar_email(contato["email"])

    return render_template("mensagens.html", contatos=contatos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
