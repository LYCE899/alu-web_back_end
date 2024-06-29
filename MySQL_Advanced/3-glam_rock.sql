-- 3-glam_rock.sql

-- Select band_name and calculate lifespan in years
SELECT 
    band_name,
    IF(split IS NULL, YEAR(CURDATE()) - formed, split - formed) AS lifespan
FROM 
    metal_bands
WHERE 
    main_style = 'Glam rock'
ORDER BY 
    lifespan DESC;
