{{ config(
    materialized='view'
) }}

SELECT
    id,
    brand_id,
    brand_name,
    created,
    modified
FROM {{ source('data_mining', 'core_brand') }}
