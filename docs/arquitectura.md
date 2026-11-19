# Arquitectura

```text
archivo .dsl
↓
DataDSLLexer
↓
DataDSLParser
↓
árbol sintáctico
↓
DataDSLVisitorImpl
├── ContextoEjecucion
├── MotorDatos
└── librerias propias
    ├── DataTable
    ├── DataMath
    ├── DataStats
    ├── DataMatrix
    ├── DataRandom
    ├── DataFiles
    ├── DataML
    └── DataGraph
```

## Responsabilidades

`DataDSL.g4` define la sintaxis. `DataDSLVisitorImpl.py` interpreta el árbol. `ContextoEjecucion.py` guarda variables y funciones. `MotorDatos.py` organiza el procesamiento tabular. `DataTable.py` contiene la estructura real de los datos.

La separación permite explicar el proyecto por módulos y evita concentrar todo en un único intérprete.
