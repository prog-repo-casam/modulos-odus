from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("north", "North"),("south", "South"),("east", "East"),("west","West")])

    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[("new", "New"),("offer_received", "Offer Received"),("offer_accepted", "Offer Accepted"),("sold", "Sold"),("canceled","Canceled")],
    required=True, copy=False, default="new")

    property_type_id = fields.Many2one("estate.property.type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.user.company_id.id, required=True)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate_property in self:
            try:
                estate_property.best_price = max(estate_property.offer_ids.mapped('price'))
            except:
                estate_property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for estate_property in self:
            if estate_property.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            estate_property.state = "sold"
        return True

    def action_cancel(self):
        for estate_property in self:
            if estate_property.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            estate_property.state = "canceled"
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for estate_property in self:
            if estate_property.selling_price > 0 and estate_property.selling_price < ((estate_property.expected_price*90)/100): #90% of expected price
                raise ValidationError("The selling price must be at least 90\% of the expected price! You must reduce the expected price if you want to accept this offer.")

    @api.ondelete(at_uninstall=False)
    def check_state_before_delete(self):
        for estate_property in self:
            if estate_property.state not in ("canceled", "new"):
                raise UserError("Only new and canceled properties can be deleted.")




       

    


