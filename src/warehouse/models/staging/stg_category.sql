{{ config(
    materialized='view'
) }}

SELECT
    id,
    category_id,
    name,
    description,
    source_channel_id,
    created,
    modified
FROM {{ source('data_mining','core_category') }}
