-- 3-glam_rock.sql
-- Lists all bands with 'Glam rock' as their main style, ranked by their longevity

-- Import the metal_bands.sql.zip table dump
-- CREATE DATABASE IF NOT EXISTS holberton;
-- USE holberton;
-- SOURCE metal_bands.sql;

SELECT 
    band_name,
    IFNULL(2022 - formed, 0) AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
