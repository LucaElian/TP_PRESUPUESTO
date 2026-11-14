from math import isfinite
from statistics import fmean

# CONFIGURACIONES

CAPITAL = 850000
CANTIDAD_ANIOS = 3
INVERSION_ANIO = 1

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


# PUNTO 1: CARGAR TASAS HISTORICAS

def cargar_historicos():
    historicos = {}

    for banco in BANCOS:
        tasas = []

        print(f"\n-- {banco} --")

        for anio in range(1, CANTIDAD_ANIOS + 1):
            while True:
                try:
                    numero = float(input(f"Ingrese la tasa historica del año {anio} (%): "))

                    if not isfinite(numero) or numero <= 0:
                        print("Error: Ingrese un numero mayor a 0")

                    tasas.append(numero)
                    break

                except ValueError:
                    print("Error: Debe ingresar un numero valido")

        historicos[banco] = tasas

    return historicos


# PUNTO 2: CALCULAR PROMEDIOS

def calcular_promedios(historicos):
    promedios = {}

    print("\n--- PROMEDIO DE TASAS ANUALES ---")

    for banco, tasas in historicos.item():
        promedio = fmean(tasas)
        promedios[banco] = promedio

        print(f"{banco}: {promedio:.2f}%")

    return promedios


# CALCULAR RENDIMIENTO

def calcular_rendimiento(tasa, cantidad_periodos):
    monto_actual = CAPITAL
    tasa_etapa = (tasa / 100) / cantidad_periodos

    for x in range(cantidad_periodos):
        ganancia_etapa = monto_actual * tasa_etapa
        monto_actual += ganancia_etapa

    return monto_actual - CAPITAL


# PUNTO 3: EVALUAR INVERSIONES

def evaluar_inversiones(promedios):
    mejor_rendimiento = -1
    mejor_banco = ""
    mejor_modalidad = ""

    print("\n--- MODALIDADES DE INVERSION ---")

    for banco, tasa in promedios.items():
        print(f"\n-- {banco} --")

        for modalidad, cantidad_periodos in MODALIDADES.items():
            rendimiento = calcular_rendimiento(tasa, cantidad_periodos)
            monto = CAPITAL + rendimiento

            print(f"{modalidad}:")
            print(f"  Rendimiento: ${rendimiento:.2f}")
            print(f"  Capital final: ${monto:.2f}")

            if rendimiento > mejor_rendimiento:
                mejor_rendimiento = rendimiento
                mejor_banco = banco
                mejor_modalidad = modalidad

    print("\n--- MEJOR OPCION DE INVERSION ---")
    print(f"Banco recomendado: {mejor_banco}")
    print(f"Modalidad recomendada: {mejor_modalidad}")
    print(f"Ganancia: ${mejor_rendimiento:.2f}")
    print(f"Capital final: ${CAPITAL + mejor_rendimiento:.2f}")


# PROGRAMA PRINCIPAL

def main():
    historicos = cargar_historicos()
    promedios = calcular_promedios(historicos)
    evaluar_inversiones(promedios)

if __name__ == "__main__":
    main()