from odoo import fields, models, api


class EstateInheritance(models.Model):
    _inherit = 'res.partner'

    sales_person = fields.One2many("real.estate", "sales_person", "RealEstate")