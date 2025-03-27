from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class Property(models.Model):
    """
    Real Estate Property model representing property listings.

    This model manages property details, including basic information, 
    pricing, characteristics, and state management.
    """

    # Private attributes
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    # Default methods
    def _default_date_availability(self):
        """
        Compute default date availability 3 months from today.

        Returns:
            date: Date 3 months from current date
        """
        return fields.Date.today() + relativedelta(months=3)

    # Fields declaration
    name = fields.Char(
        string='Title', 
        required=True,
        help="Name or title of the property listing"
    )
    description = fields.Text(
        string='Description', 
        help="Detailed description of the property"
    )
    postcode = fields.Char(
        string='Postcode', 
        help="Postal code of the property location"
    )
    date_availability = fields.Date(
        string='Available From', 
        copy=False, 
        default=_default_date_availability
    )
    expected_price = fields.Float(
        string='Expected Price', 
        required=True, 
        help="Seller's expected selling price"
    )
    selling_price = fields.Float(
        string='Selling Price', 
        readonly=True, 
        copy=False, 
        help="Final selling price of the property"
    )
    bedrooms = fields.Integer(
        string='Bedrooms', 
        default=2, 
        help="Number of bedrooms in the property"
    )
    living_area = fields.Integer(
        string='Living Area (sqm)', 
        help="Total living area in square meters"
    )
    facades = fields.Integer(
        string='Facades', 
        help="Number of building facades"
    )
    garage = fields.Boolean(
        string='Garage', 
        help="Indicates if the property has a garage"
    )
    garden = fields.Boolean(
        string='Garden', 
        help="Indicates if the property has a garden"
    )
    garden_area = fields.Integer(
        string='Garden Area (sqm)', 
        help="Total garden area in square meters"
    )
    total_area = fields.Integer(
        string="Total Area (sqm)", 
        compute="_compute_total_area", 
        help="Sum of living and garden areas"
    )
    best_price = fields.Float(
        string="Best Offer", 
        compute="_compute_best_price", 
        help="Highest offer received for the property"
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ],
        help="Orientation of the garden"
    )
    active = fields.Boolean(
        string='Active', 
        default=True, 
        help="Indicates if the property listing is active"
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ], 
        string='Status', 
        required=True, 
        copy=False, 
        default='new',
        help="Current status of the property listing"
    )
    property_type_id = fields.Many2one(
        'estate.property.type', 
        string='Property Type',
        help="Type of property"
    )
    buyer_id = fields.Many2one(
        'res.partner', 
        string='Buyer', 
        copy=False,
        help="Buyer of the property"
    )
    salesperson_id = fields.Many2one(
        'res.users', 
        string='Salesperson', 
        default=lambda self: self.env.user.id,
        help="Salesperson managing the property listing"
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        help="Tags associated with the property"
    )
    offer_ids = fields.One2many(
        'estate.property.offer', 
        'property_id', 
        string='Offers',
        help="Offers received for the property"
    )

    # Compute methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """
        Compute the total area by summing living and garden areas.
        
        Sets the total_area field for each record.
        """
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        """
        Compute the best (highest) offer price.
        
        Sets the best_price field to the maximum offer price or 0.0 if no offers.
        """
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    # Onchange methods
    @api.onchange('garden')
    def _onchange_garden(self):
        """
        Set default garden area and orientation when garden is checked.
        
        If garden is True, sets garden_area to 10 and orientation to 'north'.
        If garden is False, resets garden_area to 0 and orientation to False.
        """
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Action methods
    def action_sold(self):
        """
        Mark the property as sold.
        
        Raises a UserError if the property is in a cancelled state.
        Sets the state to 'sold' for each record.
        
        Returns:
            bool: Always returns True if successful
        
        Raises:
            UserError: If trying to sell a cancelled property
        """
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        """
        Cancel the property listing.
        
        Raises a UserError if the property is already sold.
        Sets the state to 'cancelled' for each record.
        
        Returns:
            bool: Always returns True if successful
        
        Raises:
            UserError: If trying to cancel a sold property
        """
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True

    # Constraints
    _sql_constraints = [
        ('check_expected_price', 
         'CHECK(expected_price > 0)', 
         'The expected price must be strictly positive'),
        ('check_selling_price', 
         'CHECK(selling_price > 0)', 
         'The selling price must be strictly positive')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        """
        Validate that the selling price is at least 90% of the expected price.
        
        Raises a ValidationError if the selling price is less than 90% 
        of the expected price.
        
        Raises:
            ValidationError: If selling price is below 90% of expected price
        """
        for record in self:
            if (not float_is_zero(record.selling_price, precision_rounding=0.01) and 
                float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    "You must reduce the expected price if you want to accept this offer."
                )

    # Delete method
    @api.ondelete(at_uninstall=False)
    def _unlink_except_not_new_or_cancelled(self):
        """
        Prevent deletion of properties not in 'new' or 'cancelled' states.
        
        Raises a UserError if attempting to delete a property 
        that is not in a new or cancelled state.
        
        Raises:
            UserError: If trying to delete a property that is not new or cancelled
        """
        undeletable_properties = self.filtered(
            lambda prop: prop.state not in ['new', 'cancelled']
        )
        
        if undeletable_properties:
            raise UserError("Only new and cancelled properties can be deleted")