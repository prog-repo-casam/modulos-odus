from odoo import fields, models

class Freight(models.Model):
    _name = "ca.costo.freight"
    _description = "Flete para costos"

    price = fields.Float(string="Precio", required=True)
    country_id = fields.Many2one("res.country", string="Pais", required=True)
