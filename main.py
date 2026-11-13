from math import isfinite

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
