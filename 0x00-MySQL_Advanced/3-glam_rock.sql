-- 3-glam_rock.sql
-- Listing all bands with Glam rock as their main style, ranked by their longevity

SELECT band_name,
    COALESCE(YEAR(2022) - formed, 0) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;

