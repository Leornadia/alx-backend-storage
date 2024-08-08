-- List all glam rock bands ranked by longevity
SELECT band_name, (2022 - formed) - split AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
