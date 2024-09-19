SELECT DISTINCT ON (ml_info.item_id)
    ml_info.item_id,
    ml_info.title,
    ml_info.codpro,
    ml_info.sku,
    ml_info.sold_quantity,
    ml_info.has_compatibilities,
    CASE
        WHEN ml_cat_compatibilities.categories_id IS NULL THEN FALSE
        ELSE TRUE
    END as comp_obrigatoria
FROM "ECOMM".ml_info
LEFT JOIN "ECOMM".ml_cat_compatibilities
ON ml_info.category_id = ml_cat_compatibilities.categories_id
WHERE NOT ml_info.item_id in %s;