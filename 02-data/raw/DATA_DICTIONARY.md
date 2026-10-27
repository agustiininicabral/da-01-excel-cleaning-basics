# Data Dictionary

## sales.csv — 3.500 registros
- `order_id` (text): identificador único de pedido.
- `customer_id` (text): identificador de cliente.
- `order_date` (date): fecha de compra.
- `category` (category): categoría del producto.
- `channel` (category): canal atribuido a la venta.
- `country` (category): país.
- `city` (text): ciudad.
- `quantity` (int): unidades vendidas; debe ser mayor que cero.
- `unit_price` (decimal): precio unitario.
- `discount_rate` (decimal): descuento aplicado, entre 0 y 0,20.
- `net_revenue` (decimal): ingresos netos, calculados como cantidad × precio × (1 − descuento).
- `cost` (decimal): costo estimado asociado a la venta.
- `payment_method` (category): método de pago.
- `device` (category): dispositivo asociado al pedido.

## products.csv — 500 productos
- `product_id` (text): identificador único del producto.
- `product_name` (text): nombre de producto.
- `category` (category): categoría del catálogo.
- `brand` (category): marca ficticia.
- `active` (Yes/No): indica si el producto está activo.

## Relaciones y limitaciones

- `order_id` es único en el archivo de ventas; cada fila representa un pedido.
- `sales.csv` no contiene `product_id`, por lo que ventas y catálogo solo se pueden comparar por categoría, no por producto individual.
- Los datos son sintéticos y las cifras monetarias no están asociadas a una moneda real.
