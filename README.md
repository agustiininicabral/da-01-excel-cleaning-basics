# Excel Cleaning Basics

Proyecto de portfolio de Data Analytics para limpieza, validación y análisis exploratorio de datos de ventas sintéticos.

![Data validation](https://github.com/agustiininicabral/da-01-excel-cleaning-basics/actions/workflows/ci.yml/badge.svg)

## Objetivo

Demostrar un flujo reproducible de preparación de datos: perfilado, validación de tipos y reglas, SQL básico, KPIs y documentación de insights. Los CSV originales se mantienen sin modificar.

## Dataset

- `02-data/raw/sales.csv`: 3.500 registros de ventas.
- `02-data/raw/products.csv`: catálogo de 500 productos.
- `02-data/raw/DATA_DICTIONARY.md`: descripción de campos y reglas.

Los datos son ficticios. Una fila de `sales.csv` representa un pedido, identificado por `order_id`; el catálogo se relaciona con las ventas por categoría, no por `product_id`, porque el archivo de ventas no contiene ese identificador.

## Validación reproducible

Requiere Python 3.12. En PowerShell, desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python scripts/validate_data.py
python -m pytest -q
ruff format --check scripts tests
ruff check scripts tests
```

El validador revisa columnas requeridas, celdas vacías, duplicados de identificadores, fechas, cantidades, descuentos, coherencia de ingresos netos y consistencia de categorías entre ventas y catálogo. Devuelve código de salida distinto de cero si encuentra errores. GitHub Actions ejecuta las mismas verificaciones en cada push y pull request.

## SQL

Los scripts están en `03-work/sql/`:

- `00_load_instructions.sql`: instrucciones para importar los CSV.
- `01_core_queries.sql`: consultas de ingresos por categoría, margen por canal y clientes con mayor ingreso acumulado.

Las consultas usan sintaxis compatible con PostgreSQL y SQLite. Para SQL Server, adaptá la consulta con `LIMIT` a `TOP` o `OFFSET/FETCH`.

## Resultados

El análisis y los KPIs están documentados en [05-results/report.md](05-results/report.md). Las cifras corresponden exclusivamente al dataset sintético incluido; no representan resultados de una empresa real.

## Estructura

- `01-requirements/`: preguntas de negocio, alcance e hipótesis.
- `02-data/raw/`: archivos originales y diccionario.
- `03-work/sql/`: instrucciones de carga y consultas.
- `05-results/report.md`: resultados, insights, recomendaciones y limitaciones.
- `templates/`: plantillas reutilizables.

## Licencia

MIT. Consultá [LICENSE](LICENSE).
