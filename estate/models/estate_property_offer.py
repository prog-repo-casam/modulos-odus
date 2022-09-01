from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price =  fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"),("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property_offer in self:
            try:
                t_date = property_offer.create_date.date()
                property_offer.date_deadline = t_date + relativedelta(days=property_offer.validity)
            except:
                property_offer.date_deadline = fields.Date.today() + relativedelta(days=property_offer.validity)

    def _inverse_date_deadline(self):
        for property_offer in self:
            delta = property_offer.date_deadline - property_offer.create_date.date()
            property_offer.validity = delta.days

    def action_accept(self):
        for property_offer in self:
            other_accepted = property_offer.search(['&', ('status', '=', 'accepted'), ('property_id', '=', property_offer.property_id.id)], limit=1)
            if other_accepted:
                raise UserError("Another offer has been accepted first.")
            property_offer.status = "accepted"
            if property_offer.property_id.state not in ("canceled", "sold", "offer_accepted"): #This condition is because when we use functions in offers demo data, it changes the demo estate_property state
                property_offer.property_id.state = "offer_accepted"
            property_offer.property_id.selling_price = property_offer.price
            property_offer.property_id.partner_id = property_offer.partner_id
        return True

    def action_refuse(self):
        for property_offer in self:
            property_offer.status = "refused"
        return True

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.model
    def create(self, vals):
        estate_property = self.env["estate.property"].browse(vals["property_id"])
        if vals["price"] < estate_property.best_price:
            raise UserError("The offer price amount must be higher than %s" % estate_property.best_price)
        if estate_property.state not in ("canceled", "sold", "offer_accepted"): #This condition is because when we create offers demo data, it changes the demo estate_property state
            estate_property.state = "offer_received"

        return super().create(vals)



    