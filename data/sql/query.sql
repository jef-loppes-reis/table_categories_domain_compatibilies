SELECT DISTINCT ON (ml_info.item_id)
    ml_info.item_id,
    ml_info.title,
	ml_info.status,
	ml_info.sub_status,
	CASE
		WHEN ml_info.channels in ('{marketplace,mshops}', '{mshops,marketplace}') THEN 'ML/SHOPS'
		WHEN ml_info.channels = '{mshops}' THEN 'SHOPS'
		WHEN ml_info.channels = '{marketplace}' THEN 'ML'
		ELSE ml_info.channels
	END canais_venda,
    ml_info.codpro,
    ml_info.sku,
	ml_info.storage,
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