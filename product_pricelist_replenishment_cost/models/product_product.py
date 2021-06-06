# Copyright 2021 APA! Argentina - Matias Cerutti
# Based on 2018 Tecnativa product_pricelist_supplierinfo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_replenishmentinfo_pricelist_price(self, rule, date=None, quantity=None):
        return self.product_tmpl_id._get_replenishmentinfo_pricelist_price(
            rule, date=date, quantity=quantity, product_id=self.id
        )

    def price_compute(self, price_type, uom=False, currency=False, company=False):
        """Return dummy not falsy prices when computation is done from supplier
        info for avoiding error on super method. We will later fill these with
        correct values.
        """
        if price_type == "replenishmentcost":
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company
        )
