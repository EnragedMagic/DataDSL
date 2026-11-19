# Manual de usuario

## Preparar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo apt install antlr4
bash generar_antlr.sh
```

## Ejecutar un programa

```bash
python3 main.py ejemplos/programa_final.dsl
```

## Ver resultados

```bash
ls salidas
cat salidas/resumen_final.csv
```

## Ejecutar pruebas

```bash
python3 -m unittest discover -s tests -v
```
