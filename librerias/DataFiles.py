# Lee y escribe archivos de texto cuando el programa lo solicita.

from pathlib import Path


def leer_texto(ruta):
    # Lee un archivo completo.
    return Path(str(ruta)).read_text(encoding="utf-8")


def escribir_texto(ruta, contenido):
    # Escribe un archivo nuevo.
    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(str(contenido), encoding="utf-8")
    return str(ruta)


def agregar_texto(ruta, contenido):
    # Agrega texto al final.
    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write(str(contenido))
    return str(ruta)


FUNCTIONS = {
    "leer_texto": leer_texto,
    "escribir_texto": escribir_texto,
    "agregar_texto": agregar_texto,
}
