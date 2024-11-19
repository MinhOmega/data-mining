{{ config(
    materialized='view'
) }}

SELECT
    id,
    option_name,
    created,
    modified
FROM {{ source('data_mining', 'core_productoption') }}
