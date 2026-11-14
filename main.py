from math import isfinite
import statistics

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

historicos = {}

for banco in BANCOS:
    tasas = []

    print (f"\n-- {banco} --")

    for anio in range(1, CANTIDAD_ANIOS + 1):
        while True:
            try:
                numero = float(input(f"Ingrese la tasa historica del año {anio} (%): "))

                if not isfinite(numero) or numero <= 0:
                    print(f"Error: Ingrese un numero mayor a 0.")
                    continue

                tasas.append(numero)
                break

            except ValueError:
                print("Error: debe ingresar un numero valido.")
    
    historicos[banco] = tasas

print(historicos)

for banco, tasas in historicos.items():
    promedio = statistics.fmean(tasas)
    print(f"Banco: {banco} \n Promedio de las tasas anuales: {promedio}")

def pto3(ta_bcoProvincia, ta_bcoNacion, ta_bcoHipotecario):
    tasas_bcos = [ta_bcoProvincia, ta_bcoNacion, ta_bcoHipotecario]
    mejor_rendimiento = 0
    mejor_banco = ""
    mejor_modalidad = ""
    for i in range(len(BANCOS)):
        banco = BANCOS[i]
        tasa = tasas_bcos[i]
        for modalidad, cantidadMeses in MODALIDADES.items():
            rendimiento = calcular_rendimiento( tasa, cantidadMeses)
            monto = CAPITAL + rendimiento
            #CALCULAR MAXIMO RENDIMIENTO
    #print("mejor rendimeinto es: 

def calcular_rendimiento( tasa, cantidadMeses):
    monto_actual = CAPITAL
    tasa_etapa = tasa_anual / cantidadMeses
    for x in range (cantidadMeses):
        ganancia_etapa = monto_actual * tasa_etapa
        monto_actual += ganancia_etapa
    return monto_actual - CAPITAL
    
