from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "clave_secreta"

# -------- BASE DE DATOS --------
def get_db():
    return sqlite3.connect("casino.db")

def crear_db():
    con = get_db()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            saldo INTEGER
        )
    """)
    con.commit()
    con.close()

crear_db()

# -------- INICIO --------
@app.route("/")
def inicio():
    session["usuario"] = "Kevyn"

    con = get_db()
    cursor = con.cursor()

    cursor.execute("SELECT saldo FROM usuarios WHERE nombre=?", (session["usuario"],))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO usuarios(nombre, saldo) VALUES (?,?)", (session["usuario"], 100))
        con.commit()
        saldo = 100
    else:
        saldo = user[0]

    session["saldo"] = saldo
    con.close()

    return redirect(url_for("juegos"))

# -------- JUEGOS --------
@app.route("/juegos")
def juegos():
    return render_template("juegos.html",
                           usuario=session["usuario"],
                           saldo=session["saldo"])

# -------- APOSTAR --------
@app.route("/apostar", methods=["POST"])
def apostar():
    data = request.json
    juego = data["juego"]
    apuesta = int(data["apuesta"])

    if apuesta <= 0:
        return jsonify({"resultado": "Apuesta inválida", "saldo": session["saldo"]})

    if apuesta > session["saldo"]:
        return jsonify({"resultado": "Saldo insuficiente", "saldo": session["saldo"]})

    resultado = ""
    ganancia = 0

    # 🎲 Dados
    if juego == "dados":
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        if d1 + d2 > 7:
            ganancia = apuesta
            resultado = f"🎲 {d1} + {d2} → Ganaste"
        else:
            ganancia = -apuesta
            resultado = f"🎲 {d1} + {d2} → Perdiste"

    # 🃏 Cartas
    elif juego == "cartas":
        carta = random.choice(["A","K","Q","J","10","9"])
        if carta in ["A","K"]:
            ganancia = apuesta * 2
            resultado = f"🃏 {carta} → Ganaste"
        else:
            ganancia = -apuesta
            resultado = f"🃏 {carta} → Perdiste"

    # 🎡 Ruleta
    elif juego == "ruleta":
        numero = random.randint(0,36)
        if numero % 2 == 0:
            ganancia = apuesta
            resultado = f"🎡 {numero} → Ganaste"
        else:
            ganancia = -apuesta
            resultado = f"🎡 {numero} → Perdiste"

    session["saldo"] += ganancia

    # guardar en DB
    con = get_db()
    cursor = con.cursor()
    cursor.execute("UPDATE usuarios SET saldo=? WHERE nombre=?", (session["saldo"], session["usuario"]))
    con.commit()
    con.close()

    return jsonify({
        "resultado": resultado,
        "saldo": session["saldo"]
    })

if __name__ == "__main__":
    app.run(debug=True)