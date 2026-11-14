from statistics import fmean

# CONFIGURACIONES

CAPITAL = 850000
CANTIDAD_ANIOS = 3

BANCOS = [
    "Banco Provincia", 
    "Banco Nacion", 
    "Banco Hipotecario"
]

MODALIDADES = {
    "Anual": 1,
    "Trimestral": 4,
    "Mensual": 12
}

# PUNTO 2: CALCULAR PROMEDIOS

def calcular_promedios(historicos):
    promedios = {}

    for banco, tasas in historicos.item():
        promedio = fmean(tasas)
        promedios[banco] = promedio

    return promedios


# CALCULAR RENDIMIENTO

def calcular_rendimiento(tasa, cantidad_periodos, capital):
    monto_actual = capital
    tasa_etapa = (tasa / 100) / cantidad_periodos

    for periodo in range(cantidad_periodos):
        ganancia_etapa = monto_actual * tasa_etapa
        monto_actual += ganancia_etapa

    return monto_actual - capital


# PUNTO 3: EVALUAR INVERSIONES

def evaluar_inversiones(promedios, capital):
    resultados = {}

    mejor_rendimiento = -1
    mejor_banco = ""
    mejor_modalidad = ""

    for banco, tasa in promedios.items():
        resultados[banco] = {}

        for modalidad, cantidad_periodos in MODALIDADES.items():
            rendimiento = calcular_rendimiento(tasa, cantidad_periodos, capital)

            monto = capital + rendimiento

            resultados[banco][modalidad] = {
                "ganancia": rendimiento,
                "monto_final": monto
            }

            if rendimiento > mejor_rendimiento:
                mejor_rendimiento = rendimiento
                mejor_banco = banco
                mejor_modalidad = modalidad

    recomendacion = {
        "banco": mejor_banco,
        "modalidad": mejor_modalidad,
        "ganancia": mejor_rendimiento,
        "monto_final": capital + mejor_rendimiento
    }

    return resultados, recomendacion
    main()