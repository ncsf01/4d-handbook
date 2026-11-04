import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

# Lê o arquivo .env e coloca os valores dele nas variáveis de ambiente
load_dotenv()

app = Flask(__name__)


def conectar_bd():
    """Abre uma conexão com o MySQL usando os dados do arquivo .env."""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return render_template("about.html")


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        # .strip() tira espaços sobrando no começo e no fim do texto
        email = request.form.get("email", "").strip()
        assunto = request.form.get("subject", "").strip()
        mensagem = request.form.get("message", "").strip()

        # Validação no servidor: o JavaScript da página pode ser burlado,
        # então conferimos de novo aqui antes de gravar no banco
        if not email or "@" not in email or not assunto or not mensagem:
            return redirect(url_for("contato", status="invalido"))

        try:
            conexao = conectar_bd()
            with conexao.cursor() as cursor:
                # %s = parâmetros seguros (evita SQL Injection)
                sql = "INSERT INTO contatos (email, assunto, mensagem) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email[:255], assunto[:150], mensagem))
            conexao.commit()
            conexao.close()
        except pymysql.MySQLError as erro:
            # Se o banco estiver fora do ar, o site não cai: mostra um aviso
            app.logger.error("Erro ao salvar contato: %s", erro)
            return redirect(url_for("contato", status="erro"))

        # Redireciona depois do POST para o navegador não reenviar
        # o formulário se a pessoa apertar F5
        return redirect(url_for("contato", status="enviado"))

    return render_template("contato.html", status=request.args.get("status"))


if __name__ == "__main__":
    # host="0.0.0.0" faz o Flask aceitar conexões de fora da máquina
    # (sem isso, só a própria instância consegue abrir o site).
    app.run(host="0.0.0.0", port=5000)
