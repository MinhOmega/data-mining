{{ config(
    materialized='view'
) }}

SELECT
    id,
    product_asset_id,
    product_id,
    asset_url,
    asset_type,
    position,
    created,
    modified
FROM {{ source('data_mining', 'core_productasset') }}
