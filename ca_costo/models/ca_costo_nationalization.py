from odoo import fields, models

class Nationalization(models.Model):
    _name = "ca.costo.nationalization"
    _description = "Coste de Nacionalizacion"

    price = fields.Float(string="Precio", required=True)
    product_template_id = fields.Many2one("product.template", string="Plantilla de producto", required=True)