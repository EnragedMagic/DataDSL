# Tabla tabular propia de DataDSL.

import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


class TablaDatos:
    def __init__(self, columnas, filas=None):
        # Guarda columnas y filas.
        self.columnas = list(columnas)
        self.filas = [dict(fila) for fila in (filas or [])]

    @classmethod
    def desde_csv(cls, ruta, separador=","):
        # Carga un CSV sin pandas.
        ruta = Path(str(ruta))
        if not ruta.exists():
            raise FileNotFoundError(str(ruta))

        with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
            # Las notas de procedencia opcionales van antes del encabezado.
            while True:
                posicion = archivo.tell()
                linea = archivo.readline()
                if not linea.startswith("# "):
                    archivo.seek(posicion)
                    break
            lector = csv.DictReader(archivo, delimiter=separador)
            columnas = lector.fieldnames or []
            filas = []
            for fila in lector:
                filas.append({k: _convertir_celda(v) for k, v in fila.items()})
        return cls(columnas, filas)

    @classmethod
    def desde_xlsx(cls, ruta):
        # Lee la primera hoja de un XLSX sin librerias externas.
        ruta = Path(str(ruta))
        if not ruta.exists():
            raise FileNotFoundError(str(ruta))

        with zipfile.ZipFile(ruta, "r") as archivo:
            compartidas = _leer_cadenas_xlsx(archivo)
            hoja = _ruta_primera_hoja(archivo)
            raiz = ET.fromstring(archivo.read(hoja))
            ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

            filas_crudas = []
            for fila_xml in raiz.findall(f".//{ns}sheetData/{ns}row"):
                valores = {}
                for celda in fila_xml.findall(f"{ns}c"):
                    referencia = celda.attrib.get("r", "A1")
                    indice = _indice_columna_xlsx(referencia)
                    valores[indice] = _valor_celda_xlsx(celda, compartidas, ns)
                if valores:
                    maximo = max(valores)
                    filas_crudas.append([valores.get(i) for i in range(maximo + 1)])

        if not filas_crudas:
            return cls([], [])

        columnas = [
            str(valor) if valor not in (None, "") else f"columna_{i + 1}"
            for i, valor in enumerate(filas_crudas[0])
        ]
        filas = []
        for valores in filas_crudas[1:]:
            valores = valores + [None] * (len(columnas) - len(valores))
            filas.append({
                columna: _convertir_celda(valores[i])
                for i, columna in enumerate(columnas)
            })
        return cls(columnas, filas)


    def a_csv(self, ruta, separador=","):
        # Guarda la tabla como CSV.
        ruta = Path(str(ruta))
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=self.columnas, delimiter=separador)
            escritor.writeheader()
            for fila in self.filas:
                escritor.writerow({c: _serializar(fila.get(c)) for c in self.columnas})
        return str(ruta)

    def copiar(self):
        # Crea una copia independiente.
        return TablaDatos(self.columnas, self.filas)

    def validar_columnas(self, columnas):
        # Comprueba columnas requeridas.
        for columna in columnas:
            if columna not in self.columnas:
                raise KeyError(columna)

    def tomar(self, columnas):
        # Conserva columnas elegidas.
        self.validar_columnas(columnas)
        filas = [{c: fila.get(c) for c in columnas} for fila in self.filas]
        return TablaDatos(columnas, filas)

    def filtrar(self, predicado):
        # Conserva filas que cumplen la condicion.
        filas = []
        for indice, fila in enumerate(self.filas):
            if bool(predicado(dict(fila), indice)):
                filas.append(dict(fila))
        return TablaDatos(self.columnas, filas)

    def ordenar(self, columna, direccion="asc"):
        # Ordena por una columna.
        self.validar_columnas([columna])
        reversa = direccion == "desc"

        def clave(fila):
            valor = fila.get(columna)
            # Los nulos se dejan al final.
            if valor is None:
                return (1, "")
            if isinstance(valor, (int, float, bool)):
                return (0, float(valor))
            return (0, str(valor))

        filas = sorted(self.filas, key=clave, reverse=reversa)
        return TablaDatos(self.columnas, filas)

    def crear_columna(self, nombre, generador):
        # Agrega o reemplaza una columna.
        columnas = list(self.columnas)
        if nombre not in columnas:
            columnas.append(nombre)

        filas = []
        for indice, fila in enumerate(self.filas):
            nueva = dict(fila)
            if callable(generador):
                nueva[nombre] = generador(dict(fila), indice)
            elif isinstance(generador, list):
                nueva[nombre] = generador[indice]
            else:
                nueva[nombre] = generador
            filas.append(nueva)
        return TablaDatos(columnas, filas)

    def rellenar_nulos(self, columna, valor):
        # Sustituye valores faltantes.
        self.validar_columnas([columna])
        filas = []
        for fila in self.filas:
            nueva = dict(fila)
            if nueva.get(columna) is None:
                nueva[columna] = valor
            filas.append(nueva)
        return TablaDatos(self.columnas, filas)

    def eliminar_nulos(self, columnas):
        # Borra filas con nulos.
        self.validar_columnas(columnas)
        filas = [
            dict(fila)
            for fila in self.filas
            if all(fila.get(c) is not None for c in columnas)
        ]
        return TablaDatos(self.columnas, filas)

    def eliminar_duplicados(self):
        # Elimina filas repetidas.
        vistos = set()
        filas = []
        for fila in self.filas:
            clave = tuple(_hacer_hashable(fila.get(c)) for c in self.columnas)
            if clave not in vistos:
                vistos.add(clave)
                filas.append(dict(fila))
        return TablaDatos(self.columnas, filas)

    def renombrar(self, anterior, nuevo):
        # Cambia el nombre de una columna.
        self.validar_columnas([anterior])
        if nuevo in self.columnas and nuevo != anterior:
            raise ValueError(f"La columna '{nuevo}' ya existe.")
        columnas = [nuevo if c == anterior else c for c in self.columnas]
        filas = []
        for fila in self.filas:
            nueva = {}
            for c in self.columnas:
                nueva[nuevo if c == anterior else c] = fila.get(c)
            filas.append(nueva)
        return TablaDatos(columnas, filas)

    def convertir(self, columna, tipo):
        # Convierte una columna a otro tipo.
        self.validar_columnas([columna])
        filas = []
        for fila in self.filas:
            nueva = dict(fila)
            nueva[columna] = _convertir_tipo(nueva.get(columna), tipo)
            filas.append(nueva)
        return TablaDatos(self.columnas, filas)

    def agrupar(self, columnas):
        # Agrupa filas por una o varias columnas.
        self.validar_columnas(columnas)
        return AgrupacionDatos(self, columnas)

    def columna(self, nombre, omitir_nulos=True):
        # Devuelve una columna como lista.
        self.validar_columnas([nombre])
        valores = [fila.get(nombre) for fila in self.filas]
        if omitir_nulos:
            valores = [v for v in valores if v is not None]
        return valores

    def matriz_columnas(self, columnas, omitir_nulos=True):
        # Convierte columnas en una matriz.
        self.validar_columnas(columnas)
        matriz = []
        for fila in self.filas:
            valores = [fila.get(c) for c in columnas]
            if omitir_nulos and any(v is None for v in valores):
                continue
            matriz.append(valores)
        return matriz

    def fila(self, indice):
        # Devuelve una fila por indice.
        return dict(self.filas[int(indice)])

    def nombres_columnas(self):
        # Lista los nombres de columnas.
        return list(self.columnas)

    def __len__(self):
        # Cantidad de filas.
        return len(self.filas)

    def __getitem__(self, clave):
        # Permite tabla["columna"] y tabla[indice].
        if isinstance(clave, str):
            return self.columna(clave, omitir_nulos=False)
        return self.fila(clave)

    def __str__(self):
        # Muestra una tabla corta en terminal.
        if not self.columnas:
            return "<TablaDatos vacia>"
        filas = self.filas[:12]
        anchos = {c: len(str(c)) for c in self.columnas}
        for fila in filas:
            for c in self.columnas:
                anchos[c] = max(anchos[c], len(str(_serializar(fila.get(c)))))
        encabezado = " | ".join(str(c).ljust(anchos[c]) for c in self.columnas)
        linea = "-+-".join("-" * anchos[c] for c in self.columnas)
        cuerpo = [
            " | ".join(str(_serializar(fila.get(c))).ljust(anchos[c]) for c in self.columnas)
            for fila in filas
        ]
        if len(self.filas) > len(filas):
            cuerpo.append(f"... {len(self.filas) - len(filas)} filas mas")
        return "\n".join([encabezado, linea] + cuerpo)


class AgrupacionDatos:
    def __init__(self, tabla, columnas):
        # Guarda grupos por clave.
        self.tabla = tabla
        self.columnas = list(columnas)
        self.grupos = {}
        for fila in tabla.filas:
            clave = tuple(fila.get(c) for c in self.columnas)
            self.grupos.setdefault(clave, []).append(dict(fila))

    def items(self):
        # Recorre clave y filas.
        return self.grupos.items()


def _ruta_primera_hoja(archivo):
    # Busca la primera hoja dentro del XLSX.
    workbook = ET.fromstring(archivo.read("xl/workbook.xml"))
    ns_main = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    ns_rel = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    hoja = workbook.find(f".//{ns_main}sheet")
    if hoja is None:
        raise ValueError("El XLSX no contiene hojas.")
    relacion = hoja.attrib.get(f"{ns_rel}id")

    rels = ET.fromstring(archivo.read("xl/_rels/workbook.xml.rels"))
    for item in rels:
        if item.attrib.get("Id") == relacion:
            objetivo = item.attrib["Target"].lstrip("/")
            if objetivo.startswith("xl/"):
                return objetivo
            return "xl/" + objetivo
    return "xl/worksheets/sheet1.xml"


def _leer_cadenas_xlsx(archivo):
    # Lee textos compartidos del XLSX.
    if "xl/sharedStrings.xml" not in archivo.namelist():
        return []
    raiz = ET.fromstring(archivo.read("xl/sharedStrings.xml"))
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    cadenas = []
    for item in raiz.findall(f"{ns}si"):
        partes = [nodo.text or "" for nodo in item.iter(f"{ns}t")]
        cadenas.append("".join(partes))
    return cadenas


def _indice_columna_xlsx(referencia):
    # Convierte A, B, AA en indices numericos.
    letras = re.match(r"[A-Z]+", referencia.upper())
    texto = letras.group(0) if letras else "A"
    indice = 0
    for letra in texto:
        indice = indice * 26 + (ord(letra) - ord("A") + 1)
    return indice - 1


def _valor_celda_xlsx(celda, compartidas, ns):
    # Convierte una celda XML en un valor Python.
    tipo = celda.attrib.get("t")
    if tipo == "inlineStr":
        partes = [nodo.text or "" for nodo in celda.iter(f"{ns}t")]
        return "".join(partes)

    nodo = celda.find(f"{ns}v")
    if nodo is None or nodo.text is None:
        return None
    texto = nodo.text

    if tipo == "s":
        return compartidas[int(texto)]
    if tipo == "b":
        return texto == "1"
    if tipo in {"str", "e"}:
        return texto
    return _convertir_celda(texto)


def _convertir_celda(valor):
    # Detecta tipos simples al leer CSV.
    if valor is None:
        return None
    texto = str(valor).strip()
    if texto == "":
        return None
    if texto.lower() in {"verdadero", "true"}:
        return True
    if texto.lower() in {"falso", "false"}:
        return False
    try:
        return int(texto)
    except ValueError:
        pass
    try:
        return float(texto)
    except ValueError:
        return texto


def _convertir_tipo(valor, tipo):
    # Convierte un valor individual.
    if valor is None:
        return None
    if tipo in {"numero", "entero"}:
        return int(float(valor))
    if tipo == "decimal":
        return float(valor)
    if tipo == "texto":
        return str(valor)
    if tipo == "logico":
        if isinstance(valor, str):
            return valor.strip().lower() in {"1", "true", "verdadero", "si"}
        return bool(valor)
    raise ValueError(f"Tipo desconocido: {tipo}")


def _serializar(valor):
    # Convierte valores para CSV y terminal.
    if valor is None:
        return ""
    if valor is True:
        return "verdadero"
    if valor is False:
        return "falso"
    return valor


def _hacer_hashable(valor):
    # Convierte listas en tuplas para comparar.
    if isinstance(valor, list):
        return tuple(_hacer_hashable(v) for v in valor)
    if isinstance(valor, dict):
        return tuple(sorted((k, _hacer_hashable(v)) for k, v in valor.items()))
    return valor
