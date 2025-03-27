from odoo import models, fields, api
from datetime import date, timedelta

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    # Private attributes
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

    # Field declarations
    price = fields.Float(string='Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False,
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )
    partner_id = fields.Many2one(
        'res.partner', 
        string='Partner', 
        required=True
    )
    property_id = fields.Many2one(
        'estate.property', 
        string='Property', 
        required=True
    )
    property_type_id = fields.Many2one(
        'estate.property.type', 
        string='Property Type', 
        related='property_id.property_type_id', 
        store=True
    )

    # Compute and inverse methods
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """
        Compute the deadline date based on creation date and validity period.
        
        The deadline is calculated by adding the validity period to the creation date.
        Handles cases where create_date might not be set for new records.
        """
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        """
        Compute the validity period based on the deadline date.
        
        Calculates the number of days between creation date and deadline.
        """
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            delta = offer.date_deadline - create_date
            offer.validity = delta.days

    # Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive')
    ]

    # CRUD method overrides
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to add custom validation for property offers.
        
        Ensures:
        - Offer is linked to a property
        - New offer price is higher than existing offers
        - Property state is updated
        """
        offers_to_create = []
        
        for vals in vals_list:
            property_id = vals.get('property_id')
            if not property_id:
                raise UserError("An offer must be linked to a property")
            
            property_rec = self.env['estate.property'].browse(property_id)
            
            existing_offers = self.search([
                ('property_id', '=', property_id)
            ])
            
            if existing_offers:
                max_existing_price = max(existing_offers.mapped('price'))
                if vals.get('price', 0) <= max_existing_price:
                    raise UserError(f"The offer must be higher than {max_existing_price}")
            
            offers_to_create.append(vals)
        
        offers = super().create(offers_to_create)
        
        for offer in offers:
            offer.property_id.write({'state': 'offer_received'})
        
        return offers

    # Action methods
    def action_accept(self):
        """
        Accept the property offer.
        
        - Validates no other offer is already accepted
        - Sets offer status to accepted
        - Updates property details
        - Refuses other offers for the same property
        """
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != offer.id):
                raise UserError("Another offer has already been accepted.")
            
            offer.status = 'accepted'
            
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
            
            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
            other_offers.action_refuse()
            
        return True
    
    def action_refuse(self):
        """
        Refuse the property offer by setting its status to refused.
        """
        for offer in self:
            offer.status = 'refused'
        return True