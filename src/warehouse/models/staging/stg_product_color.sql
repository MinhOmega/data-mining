{{ config(
    materialized='view'
) }}

SELECT
    id,
    color_id,
    color_name,
    url,
    position,
    created,
    modified
FROM {{ source('data_mining', 'core_productcolor') }}
