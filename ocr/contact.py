from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import *
import logging

_logger = logging.getLogger(__name__)

class User(models.Model):
    _inherit = 'res.users'
    _name = 'res.users'

    birthday = fields.Date(string=_("Date of birth"))
    place_of_birth = fields.Char(string=_("Place of birth"))
    name_of_birth = fields.Char(string=_("Name of birth"))
    nationality = fields.Char(string=_("Nationality"))

    passport_id = fields.Char(string=_("Passport ID"))

    customer_id = fields.Char()

    # address_ids = fields.One2many('real_estate.address', 'contact_id', string=_("Addresses"))
    # privat_adress = fields.One2many('real_estate.address', 'contact_id_second_adress', string=_("Private address"))

