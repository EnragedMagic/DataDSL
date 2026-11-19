# Tabla tabular propia de DataDSL.

import csv
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
            lector = csv.DictReader(archivo, delimiter=separador)
            columnas = lector.fieldnames or []
            filas = []
            for fila in lector:
                filas.append({k: _convertir_celda(v) for k, v in fila.items()})
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
