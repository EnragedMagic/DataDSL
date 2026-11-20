# Comprueba los ejercicios del tablero, incluido el MLP para XOR.

import tempfile
import unittest
import zipfile
from pathlib import Path

from librerias.DataGraph import graficar_entrenamiento, graficar_funcion
from librerias.DataML import entrenar_mlp, predecir_mlp, sigmoide
from librerias.DataMath import es_primo, factorial
from librerias.DataStats import analisis_exploratorio
from librerias.DataTable import TablaDatos


class TestTablero(unittest.TestCase):
    def test_factorial_5_y_100(self):
        # Verifica factoriales solicitados.
        self.assertEqual(factorial(5), 120)
        self.assertEqual(
            factorial(100),
            93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000,
        )

    def test_sigmoide_y_grafica(self):
        # Calcula y genera la curva sigmoide.
        self.assertAlmostEqual(sigmoide(0), 0.5, places=8)
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "sigmoide.png"
            graficar_funcion("sigmoide", -5, 5, 0.25, ruta, "Sigmoide")
            self.assertTrue(ruta.exists())
            self.assertGreater(ruta.stat().st_size, 1000)

    def test_mlp_xor_y_grafica(self):
        # Entrena un MLP propio para XOR.
        entradas = [[0, 0], [0, 1], [1, 0], [1, 1]]
        salidas = [0, 1, 1, 0]
        modelo = entrenar_mlp(entradas, salidas, 2, 1, 3000)
        self.assertEqual(predecir_mlp(modelo, entradas), salidas)

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "xor_error.png"
            graficar_entrenamiento(modelo, ruta, "XOR")
            self.assertTrue(ruta.exists())
            self.assertGreater(ruta.stat().st_size, 1000)

    def test_xlsx_y_eda(self):
        # Lee un XLSX propio y crea su EDA.
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "Data.xlsx"
            self._crear_xlsx(ruta)
            tabla = TablaDatos.desde_xlsx(ruta)
            self.assertEqual(tabla.columnas, ["edad", "ciudad", "nota"])
            self.assertEqual(len(tabla), 3)

            resumen = analisis_exploratorio(tabla)
            self.assertEqual(len(resumen), 3)
            nota = next(fila for fila in resumen.filas if fila["columna"] == "nota")
            self.assertAlmostEqual(nota["media"], 4.0)

    def test_filtro_primos(self):
        # Conserva solo numeros primos.
        tabla = TablaDatos(
            ["valor"],
            [{"valor": valor} for valor in range(1, 21)],
        )
        primos = tabla.filtrar(lambda fila, _: es_primo(fila["valor"]))
        self.assertEqual(
            primos.columna("valor"),
            [2, 3, 5, 7, 11, 13, 17, 19],
        )

    @staticmethod
    def _crear_xlsx(ruta):
        # Crea un XLSX minimo para la prueba.
        workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <sheets><sheet name="Datos" sheetId="1" r:id="rId1"/></sheets>
</workbook>"""

        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1"
 Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
 Target="worksheets/sheet1.xml"/>
</Relationships>"""

        sheet = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
 <sheetData>
  <row r="1">
   <c r="A1" t="inlineStr"><is><t>edad</t></is></c>
   <c r="B1" t="inlineStr"><is><t>ciudad</t></is></c>
   <c r="C1" t="inlineStr"><is><t>nota</t></is></c>
  </row>
  <row r="2"><c r="A2"><v>20</v></c><c r="B2" t="inlineStr"><is><t>Bogota</t></is></c><c r="C2"><v>4.5</v></c></row>
  <row r="3"><c r="A3"><v>22</v></c><c r="B3" t="inlineStr"><is><t>Cali</t></is></c><c r="C3"><v>3.5</v></c></row>
  <row r="4"><c r="A4"><v>19</v></c><c r="B4" t="inlineStr"><is><t>Bogota</t></is></c><c r="C4"><v>4.0</v></c></row>
 </sheetData>
</worksheet>"""

        tipos = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="xml" ContentType="application/xml"/>
 <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
 <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>"""

        raiz_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1"
 Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
 Target="xl/workbook.xml"/>
</Relationships>"""

        with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as archivo:
            archivo.writestr("[Content_Types].xml", tipos)
            archivo.writestr("_rels/.rels", raiz_rels)
            archivo.writestr("xl/workbook.xml", workbook)
            archivo.writestr("xl/_rels/workbook.xml.rels", rels)
            archivo.writestr("xl/worksheets/sheet1.xml", sheet)


if __name__ == "__main__":
    unittest.main()
