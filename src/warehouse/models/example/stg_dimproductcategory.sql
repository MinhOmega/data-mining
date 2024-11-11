
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data

-- Bảng Category
CREATE TABLE Category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Bảng SourceChannel
CREATE TABLE SourceChannel (
    source_channel_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INT REFERENCES Category(category_id) ON DELETE SET NULL
);

-- Bảng Product
CREATE TABLE Product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2),
    source_channel_id INT REFERENCES SourceChannel(source_channel_id) ON DELETE SET NULL
);

-- Bảng ProductSize
CREATE TABLE ProductSize (
    size_id SERIAL PRIMARY KEY,
    size_name VARCHAR(50) NOT NULL
);

-- Bảng ProductColor
CREATE TABLE ProductColor (
    color_id SERIAL PRIMARY KEY,
    color_name VARCHAR(50) NOT NULL
);

-- Bảng Brand
CREATE TABLE Brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL
);

-- Bảng ProductOption
CREATE TABLE ProductOption (
    option_id SERIAL PRIMARY KEY,
    option_name VARCHAR(255) NOT NULL
);

-- Bảng ProductAsset
CREATE TABLE ProductAsset (
    asset_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Product(product_id) ON DELETE CASCADE,
    asset_url VARCHAR(255) NOT NULL,
    asset_type VARCHAR(50) -- Ví dụ: 'image', 'video', etc.
);

-- Bảng FactProductDetail
CREATE TABLE FactProductDetail (
    fact_product_detail_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Product(product_id) ON DELETE CASCADE,
    size_id INT REFERENCES ProductSize(size_id) ON DELETE SET NULL,
    color_id INT REFERENCES ProductColor(color_id) ON DELETE SET NULL,
    brand_id INT REFERENCES Brand(brand_id) ON DELETE SET NULL,
    option_id INT REFERENCES ProductOption(option_id) ON DELETE SET NULL,
    quantity INT,
    price NUMERIC(10, 2)
);


/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
