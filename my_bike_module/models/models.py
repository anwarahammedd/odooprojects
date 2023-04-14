from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Bike(models.Model):
    _name = "bike.bikes"
    name = fields.Char(string="Bike Name")
    bike_pic = fields.Image(string="Image")
    rider_needed = fields.Boolean(default=False)
    rider_id = fields.Many2one('res.partner', string='Rider')
    fuel_type = fields.Selection(([('petrol', 'Petrol'), ('ev', 'EV'), ('diesel', 'Diesel')]), string='Fuel Type',
                                 default='petrol')
    price = fields.Float(string='Price')
    month = fields.Integer(string='Total Months')
    emi = fields.Integer(string='EMI', compute='calculate_emi_bike')
    insurance_expiry_date = fields.Date(string='Insurance Expiry')
    bike_sequence = fields.Char(string='Sequence')
    status = fields.Selection([('new', 'New'), ('used', 'Used'), ('sold', 'Sold')], string='Status', default='new')

    # def set_bike_used(self):
    #     self.status = 'used'

    def set_bike_sold(self):
        self.status = 'sold'
        template_id = self.env.ref('my_bike_module.bike_mail_template')
        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True,
                                  email_values={'email_to': 'anwarahammed007@gmail.com'})

    def calculate_emi_bike(self):
        self.emi = self.price / self.month

    # @api.model
    # def create(self, vals):
    #     vals['bike_sequence'] = self.env['ir.sequence'].next_by_code('bike.sequence')
    #     if vals['name'] == 'abcd':
    #         vals['name'] = 'bmw'
    #     if vals['month'] == 0:
    #         if vals['price'] == 0:
    #             raise ValidationError('month and price cant be 0')
    #         raise ValidationError('price must be greater than 0')
    #     if vals['month'] < 1:
    #         raise ValidationError('month must be greater than 0')
    #     if vals['price'] == 0:
    #         raise ValidationError('price must be greater than 0')
    #     result = super(Bike, self).create(vals)
    #     return result

    # def write(self, vals):
    def check(self):
        if self.month > 12:
            raise ValidationError("Month must be less than 12")
        else:
            if self.price < 100000:
                raise ValidationError('Price cannot be less than 100000')
            else:
                raise ValidationError('All Values are correct')

    def unlink(self):
        for rec in self:
            if rec.name == "Hayabusa":
                raise ValidationError("Something went wrong")
        return super(Bike, self).unlink()