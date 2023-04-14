from odoo import fields, models, api


class PropertyTags(models.Model):
    _name = "property.tag.tags"
    _order = 'id desc'
    _order = 'name'
    name = fields.Char(string="Properties of Property")

    _sql_constraints = [
        ('unique_property_tag_tags', 'unique(name)', 'A Property type with this name already exists')
    ]