# Copyright 2021 APA! Argentina - Matias Cerutti
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Replenishment cost in sales pricelists",
    "summary": "Allows to create priceslists based on replenishment cost",
    "version": "14.0",
    "category": "Sales",
    "website": "https://github.com/mcerutti/product_pricelist_replenishment_cost",
    "author": "APA! Argentina,",
    "license": "AGPL-3",
    "depends": [
        "product",
        "product_replenishment_cost",
        "product_replenishment_cost_sale_margin"
    ],    
    "data": [
        "views/product_pricelist_item_views.xml",
    ],
    "installable": True,
}
