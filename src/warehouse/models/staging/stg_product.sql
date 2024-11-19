{{ config(
    materialized='view'
) }}

SELECT
    id,
    product_id,
    code,
    name,
    url_handle,
    description,
    min_variant_price,
    max_variant_price,
    quantity_sold,
    available_quantity,
    inventory_status,
    gender,
    product_type,
    source_channel_id,
    created,
    modified
FROM {{ source('data_mining', 'core_product') }}
