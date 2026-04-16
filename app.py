from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Ruta login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        # Validación básica (puedes conectar con el login de tu amigo)
        if usuario and password:
            session["usuario"] = usuario
            return redirect(url_for("juegos"))

    return render_template("login.html")

# Ruta juegos (TU PARTE)
@app.route("/juegos")
def juegos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("juegos.html", usuario=session["usuario"])

# Juegos backend
@app.route("/dados")
def dados():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    return {"resultado": f"{d1} y {d2}"}

@app.route("/cartas")
def cartas():
    cartas = ["A","K","Q","J","10","9"]
    return {"resultado": random.choice(cartas)}

@app.route("/ruleta")
def ruleta():
    numero = random.randint(0,36)
    color = "verde" if numero == 0 else ("rojo" if numero % 2 else "negro")
    return {"resultado": f"{numero} - {color}"}

# Cerrar sesión
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)