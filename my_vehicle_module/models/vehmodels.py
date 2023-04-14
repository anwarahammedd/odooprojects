from odoo import fields,models,api

class Vehicle(models.Model):
    _name='vehicle.vehicles'
    name=fields.Char(string="Vehicle Name")
    veh_category=fields.Selection(([('car','Car'),('bike','Bike'),('commercial','Commercial')]),string='Category',
                                  default='car')
    veh_pic=fields.Image(string="Image")
    driver_needed=fields.Boolean(default=False)
    driver_id=fields.Many2one('res.partner',string='Driver')
    fuel_type=fields.Selection(([('petrol','Petrol'),('diesel','Diesel'),('ev','EV'),('cng','CNG')]),string='Fuel Type',default='Petrol')
    price=fields.Float(string='Price')
    month=fields.Integer(string='Months')
    emi=fields.Integer(string='EMI',compute='veh_emi_calculator')
    insurance_expiry_date=fields.Date(string='Insurance Expiry')
    veh_sequence=fields.Char(string='Sequence')
    status=fields.Selection([('new','New'),('used','Used'),('sold','Sold')],string='Status',default='new')

    def veh_emi_calculator(self):
        self.emi=self.price/self.month