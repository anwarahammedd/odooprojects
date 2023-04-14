from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    new_price = fields.Integer(string="Offer Price")
    partner = fields.Many2one('res.partner', string='Partner')
    offer_id = fields.Many2one("real.estate")
    create_date = fields.Date(string='Todays Date', default=fields.Date.today(), readonly=True)
    dead_line = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    validity = fields.Integer(readonly=True, string='Validity')
    status1 = fields.Selection([('accepted', 'Accept'), ('refused', 'Refuse'), ('pen', 'Pending')])
    accept = fields.Boolean()
    refused = fields.Boolean()
    offer_count=fields.Integer(string="Offers")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.dead_line = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.dead_line and record.create_date:
                record.validity = (record.dead_line - record.create_date).days
            elif record.dead_line and record.validity:
                record.create_date = record.dead_line - timedelta(days=record.validity)

    # @api.constrains('new_price')
    # def offer_price_check_function(self):
    #     for record in self:
    #         if self.new_price < 0:
    #             raise ValidationError("Offer Price Must be strictly greater than zero")
    #
    # _sql_constraints = [
    #     ('unique_status_offer', 'unique(status_offer)', 'my_field must be unique'),
    # ]
    #
    # def get_selection_values(self):
    #     selection_dict = dict(self._fields['selection_field'].selection)
    #     return selection_dict.get(self.selection_field)
