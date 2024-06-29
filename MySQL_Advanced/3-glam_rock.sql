-- Make sure you are using the correct database
USE your_database_name;

-- Query to list all bands with Glam rock as their main style, ranked by longevity
SELECT 
    band_name,
    IFNULL(YEAR(split), YEAR(CURDATE())) - YEAR(formed) AS lifespan
FROM 
    metal_bands
WHERE 
    style = 'Glam rock'
ORDER BY 
    lifespan DESC;
