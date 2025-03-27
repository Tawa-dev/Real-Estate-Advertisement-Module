from odoo import models, fields

class EstatePropertyTag(models.Model):
    """
    Real Estate Property Tag model to add categorization and tagging for properties.
    
    This model allows defining custom tags that can be associated with properties,
    with an optional color attribute for visual differentiation.
    """
    
    # Private attributes
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'
    
    # Constraint definitions
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The property tag name must be unique!')
    ]
    
    # Fields declaration
    name = fields.Char(
        string='Name', 
        required=True, 
        help='Name of the property tag'
    )
    
    color = fields.Integer(
        string='Color Index', 
        help='Optional color index for visual representation of the tag'
    )