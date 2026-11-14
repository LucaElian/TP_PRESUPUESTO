import importlib.util
import subprocess
import sys

LIBRERIAS = {
    "flask": "Flask"
}


def verificar_dependencias():
    for modulo, paquete in LIBRERIAS.items():

        if importlib.util.find_spec(modulo) is None:
            print(f"Instalando {paquete}...")

            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                paquete
            ])