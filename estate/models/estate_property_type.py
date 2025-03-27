from odoo import models, fields, api

class EstatePropertyType(models.Model):
    """
    Real Estate Property Type model to categorize property types.
    
    This model allows defining and managing different types of real estate properties,
    with support for sequencing and tracking associated properties and offers.
    """
    
    # Private attributes
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'
    
    # Constraint definitions
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique!')
    ]
    
    # Fields declaration
    name = fields.Char(
        string='Name', 
        required=True, 
        help='Name of the property type'
    )
    
    sequence = fields.Integer(
        string='Sequence', 
        default=1, 
        help='Used to order property types in lists and forms'
    )
    
    property_ids = fields.One2many(
        comodel_name='estate.property', 
        inverse_name='property_type_id', 
        string='Properties', 
        help='Properties associated with this type'
    )
    
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer', 
        inverse_name='property_type_id', 
        string='Offers', 
        help='Property offers for this type'
    )
    
    offer_count = fields.Integer(
        string='Number of Offers',
        compute='_compute_offer_count',
        help='Total number of offers for this property type'
    )
    
    # Compute methods
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """
        Compute the total number of offers for each property type.
        
        This method calculates the count of offers associated with 
        each property type record.
        """
        for record in self:
            record.offer_count = len(record.offer_ids)