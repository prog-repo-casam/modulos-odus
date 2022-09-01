from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    container_capacity_m2 = fields.Float(string="Capacidad total de contenedor en M2")
    own_freight_cost = fields.Float(string="Coste Propio de flete", readonly=True)
    own_nationalization_cost = fields.Float(string="Coste Propio de nacionalizacion", readonly=True)
    exclude_cost_update = fields.Boolean(string="¿Excluir de actualizaciones de costo?")

    freight_country_id = fields.Many2one("res.country", string="Pais del flete")


