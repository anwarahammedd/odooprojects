from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"
    new_messages = fields.Char(string='Custom Message')
    other_informations = fields.Char(string='Other Informations')
    age_emp = fields.Integer(string="Age")
    new_messages2 = fields.Char(string="New Misc")
    bike_count = fields.Integer(string="Car Count",compute='get_bike_number')

    def get_bike_number(self):
        for rec in self:
            rec.bike_count=self.env['bike.bikes'].search_count([('rider_id', '=', self.id)])

    def get_bikes(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bike',
            'view_mode': 'tree',
            'res_model': 'bike.bikes',
            'domain': [('rider_id', '=', self.id)],
            'context': "{'create':False}"
        }
