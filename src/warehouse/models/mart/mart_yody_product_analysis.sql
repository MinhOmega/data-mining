{{ config(
    materialized='table',
)}}

WITH product_stats AS (
    SELECT
        product_id,
        COUNT(*) AS total_orders,
        SUM(quantity_sold) AS total_quantity_sold,
        SUM(available_quantity) AS total_available_quantity
    FROM
        {{ ref('stg_product') }}
    GROUP BY
        product_id
)

SELECT
    product_id,
    total_orders,
    total_quantity_sold,
    total_available_quantity
FROM product_stats