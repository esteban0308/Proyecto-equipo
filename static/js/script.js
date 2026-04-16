
// ===== INICIO (deja un juego visible por defecto) =====
document.addEventListener("DOMContentLoaded", () => {
    mostrar("dados");
});

// ===== MENÚ (CAMBIAR DE JUEGO) =====
function mostrar(id) {
    document.querySelectorAll(".juego").forEach(j => j.classList.add("oculto"));
    document.getElementById(id).classList.remove("oculto");
}

// ===== 🎲 DIBUJAR DADOS CON PUNTOS =====
function dibujarDado(num, id) {
    let dado = document.getElementById(id);
    dado.innerHTML = "";

    let posiciones = {
        1:[5],
        2:[1,9],
        3:[1,5,9],
        4:[1,3,7,9],
        5:[1,3,5,7,9],
        6:[1,3,4,6,7,9]
    };

    for(let i=1;i<=9;i++){
        let punto = document.createElement("div");

        if(posiciones[num].includes(i)){
            punto.classList.add("punto");
        }

        dado.appendChild(punto);
    }
}

// ===== 🎲 DADOS =====
function apostarDados() {
    let apuesta = document.getElementById("apuestaDados").value;

    if(!apuesta || apuesta <= 0){
        alert("Ingresa una apuesta válida");
        return;
    }

    let d1 = document.getElementById("dado1");
    let d2 = document.getElementById("dado2");

    d1.classList.add("animar");
    d2.classList.add("animar");

    setTimeout(() => {
        d1.classList.remove("animar");
        d2.classList.remove("animar");

        apostar("dados", "apuestaDados");
    }, 800);
}

// ===== 🃏 CARTAS =====
function apostarCartas() {
    let apuesta = document.getElementById("apuestaCartas").value;

    if(!apuesta || apuesta <= 0){
        alert("Ingresa una apuesta válida");
        return;
    }

    let carta = document.getElementById("carta");

    carta.classList.add("flip");

    setTimeout(() => {
        carta.classList.remove("flip");
        apostar("cartas", "apuestaCartas");
    }, 600);
}

// ===== 🎡 RULETA =====
function apostarRuleta() {
    let apuesta = document.getElementById("apuestaRuleta").value;

    if(!apuesta || apuesta <= 0){
        alert("Ingresa una apuesta válida");
        return;
    }

    let ruleta = document.getElementById("ruletaAnim");

    let giro = Math.floor(Math.random() * 2500) + 1500;

    ruleta.style.transition = "transform 3s ease-out";
    ruleta.style.transform = "rotate(" + giro + "deg)";

    setTimeout(() => {
        apostar("ruleta", "apuestaRuleta");
    }, 3000);
}

// ===== 💰 FUNCIÓN GENERAL =====
function apostar(juego, inputId) {

    let apuesta = document.getElementById(inputId).value;

    fetch("/apostar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            juego: juego,
            apuesta: apuesta
        })
    })
    .then(res => res.json())
    .then(data => {

        // RESULTADO
        let resultado = document.getElementById("resultado");
        resultado.innerText = data.resultado;

        // COLOR RESULTADO
        if (data.resultado.includes("Ganaste")) {
            resultado.style.color = "#00ff88";
        } else {
            resultado.style.color = "#ff4d4d";
        }

        // SALDO
        document.getElementById("saldo").innerText = data.saldo;

        // 🎲 DADOS VISUALES
        if (data.extra && data.extra.d1) {
            dibujarDado(data.extra.d1, "dado1");
            dibujarDado(data.extra.d2, "dado2");
        }

        // 🃏 CARTA VISUAL
        if (data.extra && data.extra.carta) {
            document.getElementById("carta").innerText = data.extra.carta;
        }

        // 🧾 HISTORIAL
        let historial = document.getElementById("historial");

        let item = document.createElement("p");
        item.innerText = data.resultado;

        if (data.resultado.includes("Ganaste")) {
            item.style.color = "#00ff88";
        } else {
            item.style.color = "#ff4d4d";
        }

        historial.prepend(item);

        // LIMPIAR INPUT
        document.getElementById(inputId).value = "";
    })
    .catch(() => {
        alert("Error al conectar con el servidor");
    });
}