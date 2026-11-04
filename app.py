from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return render_template("about.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


if __name__ == "__main__":
    # host="0.0.0.0" faz o Flask aceitar conexões de fora da máquina
    # (sem isso, só a própria instância consegue abrir o site).
    app.run(host="0.0.0.0", port=5000)
