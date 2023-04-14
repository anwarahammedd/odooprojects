from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Properties'
    status = fields.Selection(([('new', 'New'), ('cancelled', 'Cancelled'), ('sold', 'Sold')]), default='new',
                              string='Status')
    name = fields.Char(string="Name")
    property_type = fields.Many2one('property.type.types', string='Property Type', required=True)
    properties = fields.Many2many('property.tag.tags')
    place = fields.Char(string="Place", required=True)
    sales_person = fields.Many2one("res.partner", string="Sales Person")
    buyer_name = fields.Many2one("res.partner", string="Buyer Name")
    active = fields.Boolean(default=True, string='Active')
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Date Availability", default=fields.Date.today())
    expected_price = fields.Float(string="Expected Price", compute='expected_price_check_function', readonly=False,
                                  store=True)
    selling_price = fields.Float(string="Selling Price", readonly=False, compute='change_selling_price',
                                 store=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),
                                           ('east', 'East'), ('west', 'West')],
                                          string="Garden Orientation")
    last_seen = fields.Datetime(string="Last Seen", default=lambda self: fields.Datetime.now())
    # new_price = fields.One2many('estate.property.offer', string='Price')
    status_offer = fields.One2many('estate.property.offer', 'offer_id', 'PropertyOffer')
    best_offer = fields.Integer(string='Best Offer')
    dead_line = fields.Datetime(string="Deadline")
    total_area = fields.Integer(string="Total Area", compute='compute_sum')
    status2 = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold')],
        default='new',
        string='Status')
    offer_count = fields.Integer(string="Offers")


    @api.onchange('date_availability')
    def change(self):
        today = fields.Date.today()
        max_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')
        if str(self.date_availability) > max_date:
            raise ValidationError("You can only select dates within the next three months.")
        else:
            store = True

    @api.onchange('offers')
    def calculate(self):
        best_offer = 0
        for rec in self.offers:
            if rec.new_price > best_offer:
                best_offer = rec.new_price
        self.best_offer = best_offer

    @api.depends('living_area', 'garden_area')
    def compute_sum(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def property_cancelled(self):
        self.status = 'cancelled'

    def property_sold(self):
        if self.status == 'cancelled':
            raise ValidationError("Error")
        else:
            self.status = 'sold'
            self.status2='sold'

    @api.constrains('expected_price')
    def expected_price_check_function(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("Expected price must be strictly positive")

    @api.constrains('selling_price')
    def selling_price_check_function(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("Selling Price must be strictly positive")

    @api.constrains('selling_price')
    def check_selling_price_not_lower_than_expected_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError('Selling Price Cannot Be Lower Than 90% of the expected price.')

    @api.constrains('buyer_name', 'sales_person')
    def buyer_seller_not_same(self):
        for rec in self:
            if rec.sales_person == rec.buyer_name:
                raise ValidationError("Both Should Be Different")

    @api.onchange('status_offer')
    def change_selling_price(self):
        for rec in self.status_offer:
            if rec.status1 == 'accepted':
                self.selling_price = rec.new_price
                self.buyer_name = rec.partner

    @api.onchange("status_offer")
    def tick(self):
        for rec in self.status_offer:
            if rec.status1 == 'accepted':
                for recc in self.status_offer:
                    if recc.status1 != 'accepted':
                        recc.refused = True

    @api.onchange('status_offer')
    def check(self):
        for rec in self.status_offer:
            if rec.accept is True:
                rec.status1 = 'accepted'
            if rec.refused is True:
                rec.status1 = 'refused'
            if rec.accept is False and rec.refused is False:
                rec.status1 = 'pen'

            if rec.status1 == 'accepted':
                self.selling_price = rec.new_price

            if rec is not None:
                self.status2 = 'offer_received'
            if rec.status1 == 'accepted':
                self.status2 = 'offer_accepted'

    def cancel_property(self):
        self.status = 'new'

    @api.model
    def search(self,args,offset=0,limit=None,order=None,count=False):
        if self._context.get('living_area_min'):
            args=expression.AND([args,[('living_area','>=',self._context['living_area_min'])]])
        return super(RealEstate,self).search(args,offset=offset,limit=limit,order=order,count=count)