# -*- coding: utf-8 -*-
# class my_first_module(models.Model):
#     _name = 'my_first_module.my_first_module'
#     _description = 'my_first_module.my_first_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models,fields,api


class Car(models.Model):
    _name = "car.car"

    name = fields.Char(string="Car Name")
    image= fields.Image(string="Image")
    horse_power = fields.Integer(string="Horse Power")
    door_number = fields.Integer(string="Door Number")
    driver_id = fields.Many2one('res.partner', string="Driver")
    parking_id=fields.Many2one('parking.parking',string="Parking")
    features=fields.Many2many('feature.feature',string="Features")
    top_speed=fields.Integer(string="Top Speed",compute="get_total_speed")
    driver_hi=fields.Char(string="Message",compute="say_hi")
    status=fields.Selection(([('new','New'),('used','Used'),('sold','Sold')]),string="Status",default="new")

    def set_car_to_used(self):
        self.status='used'

    def set_car_to_sold(self):
        self.status='sold'

    def say_hi(self):
        self.driver_hi='Hello ' + self.driver_id.name

    def get_total_speed(self):
        self.top_speed = self.horse_power**(1/3)*40


class Parking(models.Model):
    _name="parking.parking"
    name=fields.Char(string="Name")
    car_ids=fields.One2many('car.car','parking_id',string="Cars")

class CarFeature(models.Model):
    _name="feature.feature"
    name=fields.Char(string="features")
