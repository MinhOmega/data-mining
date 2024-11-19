{{ config(
    materialized='view'
) }}

SELECT
    id,
    channel_id,
    name,
    description,
    created,
    modified
FROM {{ source('data_mining', 'core_sourcechannel') }}
