# Módulo 3 — Optimización de Base de Datos
## SQL / PL/SQL — Seguros Bolívar

---

## Consulta Original (Lenta)

```sql
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    o.total_amount
FROM
    orders o
JOIN
    customers c ON o.customer_id = c.customer_id
WHERE
    c.country = 'México';
```

**Problema:** La tabla `orders` tiene 10 millones de registros y `customers`
500,000. Sin índices ni optimización, esta consulta hace un **full scan**
de ambas tablas en cada ejecución.

---

## Estrategias de Optimización

### Estrategia 1 — Índices Compuestos

Crear índices en las columnas usadas en el `JOIN` y el `WHERE`:

```sql
-- Índice en customers para filtrar por país y hacer JOIN eficiente
CREATE INDEX idx_customers_country_id
ON customers (country, customer_id, customer_name);

-- Índice en orders para el JOIN con customers
CREATE INDEX idx_orders_customer_id
ON orders (customer_id, order_id, order_date, total_amount);
```

**¿Por qué funciona?**
- El motor de BD puede usar `idx_customers_country_id` para encontrar
  rápidamente todos los clientes de México sin recorrer toda la tabla
- El `idx_orders_customer_id` permite hacer el JOIN directamente por índice
  sin acceder a las filas completas de `orders`
- Se elimina el **full table scan** en ambas tablas

---

### Estrategia 2 — Vista Materializada

Pre-computar el resultado de la consulta y almacenarlo físicamente:

```sql
-- En Oracle
CREATE MATERIALIZED VIEW mv_orders_mexico
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    o.total_amount
FROM
    orders o
JOIN
    customers c ON o.customer_id = c.customer_id
WHERE
    c.country = 'México';

-- Consulta ahora es instantánea
SELECT * FROM mv_orders_mexico;

-- Refrescar cuando los datos cambien
BEGIN
    DBMS_MVIEW.REFRESH('mv_orders_mexico');
END;
```

**¿Por qué funciona?**
- La consulta pesada se ejecuta **una sola vez** y el resultado se almacena
- Las consultas frecuentes leen directamente de la vista materializada
- Ideal cuando los datos de México no cambian en tiempo real
- El refresco se puede programar en horarios de baja carga (ej. madrugada)

---

### Estrategia 3 — Particionamiento de Tablas

Dividir la tabla `orders` en particiones más pequeñas para reducir
el volumen escaneado:

```sql
-- Particionar orders por rango de fecha (Oracle)
CREATE TABLE orders (
    order_id      NUMBER,
    order_date    DATE,
    customer_id   NUMBER,
    total_amount  NUMBER
)
PARTITION BY RANGE (order_date) (
    PARTITION p_2024 VALUES LESS THAN (DATE '2025-01-01'),
    PARTITION p_2025 VALUES LESS THAN (DATE '2026-01-01'),
    PARTITION p_2026 VALUES LESS THAN (DATE '2027-01-01')
);
```

**¿Por qué funciona?**
- Al filtrar por fecha, Oracle hace **partition pruning** — solo lee
  las particiones relevantes en vez de los 10 millones de registros
- Cada partición es una estructura independiente, más pequeña y rápida
- Se puede combinar con índices locales por partición para mayor rendimiento
- El mantenimiento (backups, purgas) también es más eficiente por partición

---

## Resumen de Impacto Esperado

| Estrategia | Complejidad | Impacto | Mejor para |
|------------|-------------|---------|------------|
| Índices compuestos | Baja | Alto | Consultas frecuentes con JOIN y WHERE |
| Vista materializada | Media | Muy alto | Datos que no cambian en tiempo real |
| Particionamiento | Alta | Alto | Tablas con crecimiento continuo por fecha |

**Recomendación:** Aplicar las tres estrategias en conjunto. Primero los
índices (impacto inmediato), luego la vista materializada (para reportes),
y finalmente el particionamiento (para escalar a largo plazo).
