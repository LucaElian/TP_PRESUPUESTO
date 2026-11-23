from dependencias import verificar_dependencias

verificar_dependencias()

from flask import Flask, render_template, request
from math import isfinite

from calculos import (
    CAPITAL,
    BANCOS,
    CANTIDAD_ANIOS,
    MODALIDADES,
    calcular_promedios,
    evaluar_inversiones
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    promedios = None
    resultados = None
    recomendacion = None
    error = None
    historicos = {}
    campo = None
    campo_error = None

    if request.method == "POST":
        try:
            # PUNTO 1: RECIBIR LAS TASAS HISTORICAS
            for banco in BANCOS:
                tasas = []

                for anio in range(1, CANTIDAD_ANIOS + 1):
                    campo = f"{banco}_{anio}"
                    numero = float(request.form[campo])

                    if not isfinite(numero) or numero < 0:
                        raise ValueError("Tasa invalida")

                    tasas.append(numero)

                historicos[banco] = tasas


            # PUNTO 2: CALCULAR PROMEDIOS
            promedios = calcular_promedios(historicos)


            # PUNTO 3: EVALUAR INVERSIONES
            resultados, recomendacion = evaluar_inversiones(promedios, CAPITAL)

        except(ValueError, KeyError):
            error = "Ingresá tasas numéricas válidas, iguales o mayores que cero."
            campo_error = campo

    return render_template(
        "index.html",
        bancos=BANCOS,
        cantidad_anios=CANTIDAD_ANIOS,
        capital=CAPITAL,
        promedios=promedios,
        resultados=resultados,
        recomendacion=recomendacion,
        error=error,
        campo_error=campo_error,
        historicos=historicos,
        modalidades=MODALIDADES,
        form_values=request.form
    )

if __name__ == "__main__":
    import os
    import logging
    import flask.cli

    flask.cli.show_server_banner = lambda *args: None
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("\n=====================================")
        print("       SIMULADOR DE INVERSIONES")
        print("=====================================")
        print("\nServidor iniciado.")
        print("Acceder desde: http://127.0.0.1:5000")
        print("\nPresiona CTRL+C para detener.\n")

    app.run(debug=False, use_reloader=True)
