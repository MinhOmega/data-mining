{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT
        -- Lấy toàn bộ JSON từ bảng source
        product_data
    FROM {{ source('data_mining', 'core_coreproduct') }}
),

parsed_data AS (
    SELECT
        -- Ánh xạ các trường JSON đơn giản
        (product_data->>'id')::INTEGER AS id,
        product_data->>'code' AS code,
        product_data->>'name' AS name,
        (product_data->>'min_variant_price')::NUMERIC AS min_variant_price,
        (product_data->>'max_variant_price')::NUMERIC AS max_variant_price,
        product_data->>'gender' AS gender,
        product_data->>'product_type' AS product_type,
        (product_data->>'created_date')::TIMESTAMP AS created,
        (product_data->>'updated_date')::TIMESTAMP AS modified
    FROM raw_data
)

SELECT * FROM parsed_data
