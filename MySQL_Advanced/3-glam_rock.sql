-- Verify specific results
SELECT 
    band_name,
    IF(split IS NULL, YEAR(CURDATE()) - formed, YEAR(split) - formed) AS lifespan
FROM 
    metal_bands
WHERE 
    main_style = 'Glam rock'
ORDER BY 
    lifespan DESC
LIMIT 5;
