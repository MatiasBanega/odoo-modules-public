# Copyright 2021 APA! Argentina - Matias Cerutti
# Based on 2018 Tecnativa product_pricelist_supplierinfo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import datetime

from odoo import fields, models, tools


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_replenishmentinfo_pricelist_price(
        self, rule, date=None, quantity=None, product_id=None
    ):
        """Method for getting the price from supplier info."""
        self.ensure_one()
        price = 0.0
        product = self.product_variant_id
        if product_id:
            product = product.browse(product_id)
        replenishment_cost = product.replenishment_cost
        # The product_variant_id returns empty recordset if template is not
        # active, so we must ensure variant exists or _select_seller fails.
        if product:
            if type(date) == datetime:
                date = date.date()
            seller = product._select_seller(
                partner_id=rule.filter_supplier_id, quantity=quantity, date=date
            )
            if seller:
                price = replenishment_cost
        if price:
            # We need to convert the price if the pricelist and seller have
            # different currencies so the price have the pricelist currency
            if product.replenishment_cost_type in ['supplier_price', 'last_supplier_price']:
                replenishment_base_cost = product.supplier_price
                base_cost_currency = product.supplier_currency_id
            elif product.replenishment_cost_type == 'manual':
                replenishment_base_cost = product.replenishment_base_cost
                base_cost_currency = product.replenishment_base_cost_currency_id

            replenishment_cost = base_cost_currency._convert(
                replenishment_base_cost, rule.currency_id,
                self.env.company, date, round=False)
            price = replenishment_cost

            # We have to replicate this logic in this method as pricelist
            # method are atomic and we can't hack inside.
            # Verbatim copy of part of product.pricelist._compute_price_rule.
            qty_uom_id = self._context.get("uom") or self.uom_id.id
            price_uom = self.env["uom.uom"].browse([qty_uom_id])

            # We need to convert the price to the uom used on the sale, if the
            # uom on the seller is a different one that the one used there.
            if seller and seller.product_uom != price_uom:
                price = seller.product_uom._compute_price(price, price_uom)
            price_limit = price
            price = (price - (price * (rule.price_discount / 100))) or 0.0
            if rule.price_round:
                price = tools.float_round(price, precision_rounding=rule.price_round)
            if rule.price_surcharge:
                price_surcharge = self.uom_id._compute_price(
                    rule.price_surcharge, price_uom
                )
                price += price_surcharge
            if rule.price_min_margin:
                price_min_margin = self.uom_id._compute_price(
                    rule.price_min_margin, price_uom
                )
                price = max(price, price_limit + price_min_margin)
            if rule.price_max_margin:
                price_max_margin = self.uom_id._compute_price(
                    rule.price_max_margin, price_uom
                )
                price = min(price, price_limit + price_max_margin)
        return price

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
