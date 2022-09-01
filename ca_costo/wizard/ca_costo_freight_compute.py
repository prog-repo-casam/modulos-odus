from odoo import models

class CaCostoFreightCompute(models.TransientModel):
    _name = "ca.costo.freight.compute"
    _description = "Actualizar el coste del flete de los productos"

    def recalculate_products_freight_cost(self):
        freights = self.env["ca.costo.freight"].sudo().search([])
        for freight in freights:
            products = self.env['product.product'].sudo().search([])
            for product in products:
                if product.freight_country_id.id == freight.country_id.id:
                    if not product.container_capacity_m2 or product.exclude_cost_update:
                        continue
                    product.standard_price = (product.standard_price - product.own_freight_cost) + (freight.price / product.container_capacity_m2)
                    product.own_freight_cost = freight.price / product.container_capacity_m2
        return True