from pathlib import Path
import base64, bz2, csv, io, zipfile
from xml.sax.saxutils import escape

BASE = Path(__file__).resolve().parent
raiz = BASE.parent if BASE.name == '.data_upload' else BASE
partes = ''.join(p.read_text().strip() for p in sorted((raiz / '.data_upload').glob('part*.txt')))
csv_bytes = bz2.decompress(base64.b64decode(partes))
filas = list(csv.reader(io.StringIO(csv_bytes.decode('utf-8'))))

def col(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

def celda(ref, valor, encabezado=False):
    if encabezado:
        return f'<c r="{ref}" t="inlineStr"><is><t>{escape(valor)}</t></is></c>'
    try:
        int(valor)
        return f'<c r="{ref}"><v>{valor}</v></c>'
    except ValueError:
        try:
            float(valor)
            return f'<c r="{ref}"><v>{valor}</v></c>'
        except ValueError:
            return f'<c r="{ref}" t="inlineStr"><is><t>{escape(valor)}</t></is></c>'

sheet_rows = []
for i, fila in enumerate(filas, 1):
    cells = ''.join(celda(f'{col(j)}{i}', v, i == 1) for j, v in enumerate(fila, 1))
    sheet_rows.append(f'<row r="{i}">{cells}</row>')

sheet = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + ''.join(sheet_rows) + '</sheetData></worksheet>'
workbook = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
           '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Datos" sheetId="1" r:id="rId1"/></sheets></workbook>'
rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>'
root_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'

salida = raiz / 'Data.xlsx'
with zipfile.ZipFile(salida, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr('[Content_Types].xml', types)
    z.writestr('_rels/.rels', root_rels)
    z.writestr('xl/workbook.xml', workbook)
    z.writestr('xl/_rels/workbook.xml.rels', rels)
    z.writestr('xl/worksheets/sheet1.xml', sheet)
print(salida)
