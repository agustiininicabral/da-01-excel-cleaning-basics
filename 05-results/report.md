# Reporte de análisis — Excel Cleaning Basics

## Pregunta de negocio

¿Cómo se distribuyen los ingresos y el margen estimado entre categorías y canales, y qué clientes concentran más ingresos dentro del dataset de demostración?

## Hipótesis

- Los canales pagos pueden generar más ingresos, pero con un margen algo menor.
- Algunas categorías podrían concentrar una proporción relevante de los ingresos.
- Una parte importante de los clientes vuelve a comprar.

## KPIs del dataset sintético

| KPI | Resultado |
|---|---:|
| Registros de ventas / pedidos | 3.500 |
| Productos en catálogo | 500 |
| Clientes únicos | 877 |
| Unidades vendidas | 10.602 |
| Ingresos netos | 608.810,14 |
| Costo estimado | 364.075,27 |
| Margen bruto estimado | 244.734,87 |
| Tasa de margen estimada | 40,20% |
| Ingreso medio por pedido | 173,95 |
| Descuento medio por registro | 6,96% |

Las cifras están expresadas en unidades monetarias sintéticas, no en una moneda real.

## Insights

1. **El margen estimado global es 40,20%.** Los ingresos netos suman 608.810,14 frente a un costo estimado de 364.075,27. La métrica no incluye gastos operativos, marketing ni costos fijos.
2. **Las categorías líderes están relativamente equilibradas.** Infantil genera 105.711,81 (17,36% del ingreso), OTC 104.438,16 (17,16%) y Perfumería 103.784,47 (17,05%). Las tres juntas representan aproximadamente 51,56% del ingreso.
3. **Paid Social lidera por una diferencia pequeña.** Registra 95.217,15, seguido por Email con 94.856,04. La diferencia es de solo 361,11, por lo que el orden no debería interpretarse como una ventaja comercial fuerte.
4. **El margen de Organic es ligeramente superior al de Paid Social.** Organic presenta 40,73% frente a 39,79% para Paid Social, una diferencia de 0,94 puntos porcentuales. Esto es compatible con la hipótesis inicial, pero no demuestra causalidad ni incorpora costos de adquisición de clientes.
5. **805 de los 877 clientes únicos tienen más de un registro de compra.** Es aproximadamente 91,79% de los clientes del dataset. Como los datos son sintéticos, no debe tomarse como una tasa de retención real.
6. **Los controles de calidad básicos pasan en el dataset publicado.** Hay 3.500 ventas y 500 productos, sin IDs de pedido o producto duplicados, sin celdas vacías, con cantidades positivas, descuentos dentro de 0–20%, ingresos netos coherentes con cantidad/precio/descuento y categorías alineadas entre ventas y catálogo.

## Recomendaciones

- Para un caso real, comparar ingresos y margen después de incorporar gasto de marketing por canal, no solo el canal atribuido a la venta.
- Añadir una dimensión de producto con `product_id` en las ventas para relacionar pedidos y catálogo a nivel de producto.
- Crear cohortes mensuales de primera compra y calcular retención por cliente, no inferir retención únicamente a partir de pedidos repetidos.
- Automatizar la validación en el proceso de carga y conservar un reporte de errores por archivo recibido.
- Añadir pruebas de regresión para las métricas SQL y documentar la granularidad de cada tabla.

## Riesgos y limitaciones

- Dataset completamente ficticio; los resultados no son evidencia de desempeño de una empresa real.
- El costo es estimado y el margen no equivale a beneficio neto.
- El campo de canal no incluye costos de adquisición, atribución multicanal ni ventanas de conversión.
- La relación entre ventas y catálogo se realiza por categoría porque no hay `product_id` en el archivo de ventas.
- Los registros repetidos de clientes no sustituyen un análisis formal de cohortes o retención.

## Próximos pasos

- Ejecutar el validador y las consultas SQL en cada actualización del dataset.
- Documentar los pasos equivalentes de Power Query y capturar evidencia reproducible.
- Ampliar el modelo con un identificador de producto en ventas y métricas de cohortes.
