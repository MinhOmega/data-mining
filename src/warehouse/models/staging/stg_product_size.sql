{{ config(
    materialized='view'
) }}

SELECT
    id,
    size_id,
    size_name,
    position,
    created,
    modified
FROM {{ source('data_mining', 'core_productsize') }}
