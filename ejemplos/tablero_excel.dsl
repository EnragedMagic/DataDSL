# Punto 4: EDA de un archivo Excel.
# Copia Data.xlsx en la raiz del proyecto.
datos_excel := abrir "Data.xlsx";
resumen_eda := eda(datos_excel);

imprimir resumen_eda;
guardar resumen_eda como "salidas/eda_data.csv";
