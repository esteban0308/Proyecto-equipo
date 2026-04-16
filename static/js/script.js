function jugar(ruta) {
    fetch(ruta)
        .then(res => res.json())
        .then(data => {
            document.getElementById("resultado").innerText =
                "Resultado: " + data.resultado;
        });
}