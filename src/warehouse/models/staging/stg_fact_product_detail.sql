{{ config(
    materialized='view'
) }}

SELECT
    id,
    product_option_id,
    name,
    product_id,
    size_id,
    color_id,
    brand_id,
    option_id,
    quantity,
    price,
    created,
    modified
FROM {{ source('data_mining', 'core_factproductdetail') }}
