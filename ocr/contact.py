# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import *
import logging

_logger = logging.getLogger(__name__)

class User(models.Model):
    _inherit = 'res.users'
    _name = 'res.users'

    birthday = fields.Date(string=_("Geburtsdatum"))
    place_of_birth = fields.Char(string=_("Geburtsort"))
    name_of_birth = fields.Char(string=_("Geburtsname"))
    nationality = fields.Char(string=_("Nationalität"))

    passport_id = fields.Char(string=_("Dokument ID"))

    customer_id = fields.Char()

    # address_ids = fields.One2many('real_estate.address', 'contact_id', string=_("Addresses"))
    # privat_adress = fields.One2many('real_estate.address', 'contact_id_second_adress', string=_("Private address"))

