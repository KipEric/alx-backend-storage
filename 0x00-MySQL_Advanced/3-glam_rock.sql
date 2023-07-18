SELECT
  band_name,
  IFNULL(YEAR('2022') - formed, 0) - IFNULL(YEAR('2022') - split, 0) AS lifespan
FROM
  metal_bands
WHERE
  style LIKE '%Glam rock%'
ORDER BY
  lifespan DESC;
