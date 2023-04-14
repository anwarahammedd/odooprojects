from odoo import fields, models


class PropertyType(models.Model):
    _name = 'property.type.types'
    _order = 'id desc'
    _order = 'name'
    name = fields.Char(string="Property Type")
    property_id = fields.One2many("real.estate", 'property_type', 'RealEstate')
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [
        ('unique_property_type_types_name', 'unique(name)', 'A property type with this name already exists.')]
