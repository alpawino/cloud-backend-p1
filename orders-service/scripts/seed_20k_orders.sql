WITH current_orders AS (
    SELECT COUNT(*) AS current_count FROM orders
),
missing_orders AS (
    SELECT GREATEST(20000 - current_count, 0) AS rows_to_insert
    FROM current_orders
)
INSERT INTO orders (user_id, status, total, created_at)
SELECT
    ((gs - 1) % 1000) + 1 AS user_id,
    CASE (gs % 4)
        WHEN 0 THEN 'CREATED'
        WHEN 1 THEN 'PAID'
        WHEN 2 THEN 'SHIPPED'
        ELSE 'CANCELLED'
    END AS status,
    ROUND(CAST((((gs % 25) + 1) * 12.50) + (((gs % 7) + 1) * 3.75) AS numeric), 2) AS total,
    NOW() - ((gs % 30) || ' days')::interval AS created_at
FROM missing_orders,
generate_series(1, (SELECT rows_to_insert FROM missing_orders)) AS gs;

WITH current_details AS (
    SELECT COUNT(*) AS current_count FROM order_details
),
missing_details AS (
    SELECT GREATEST(20000 - current_count, 0) AS rows_to_insert
    FROM current_details
),
recent_orders AS (
    SELECT id
    FROM orders
    ORDER BY id DESC
    LIMIT (SELECT rows_to_insert FROM missing_details)
)
INSERT INTO order_details (order_id, product_id, quantity, unit_price, line_total)
SELECT
    o.id,
    ((o.id - 1) % 5000) + 1 AS product_id,
    ((o.id - 1) % 4) + 1 AS quantity,
    ROUND(CAST(((o.id % 20) + 1) * 5.25 AS numeric), 2) AS unit_price,
    ROUND(CAST(((((o.id - 1) % 4) + 1) * (((o.id % 20) + 1) * 5.25)) AS numeric), 2) AS line_total
FROM recent_orders o;
