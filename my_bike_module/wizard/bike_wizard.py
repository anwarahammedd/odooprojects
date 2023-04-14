from odoo import fields, models, api


class BikeWizard(models.TransientModel):
    _name = 'bike.wizard'
    _description = "Bike Wizard"

    price_plus = fields.Integer('Price Plus')

    def add_price(self):
        print('bike_id', self.env.context.get('active_id'))
        print('new price', self.price_plus)
        self.env['bike.bikes'].browse(self.env.context.get('active_id')).write({'price': self.price_plus})

        return {'type': 'ir.actions.act_window_close'}
