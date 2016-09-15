# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from lxml import etree
import logging

_logger = logging.getLogger(__name__)

class User(models.Model):
    _inherit = 'res.users'
    _name = 'res.users'

    surname = fields.Char(string=_("First name"), required=True)
    birthday = fields.Date(string=_("Birth date"))
    place_of_birth = fields.Char(string=_("Birth place"))
    name_of_birth = fields.Char(string=_("Maiden name"))
    nationality = fields.Char(string=_("Nationality"))
    customer_id = fields.Char()

    def _get_company_id(self):
        return

    # privat_adress = fields.One2many('real_estate.address', 'contact_id_second_adress', string=_("Private address"))

    @api.model
    def create(self, vals):
        if not vals['company_id']:
            vals['company_id'] = self.env.user.company_id.id
        return super(User, self).create(vals)


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(User, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':

            doc = etree.XML(res['arch'])

            for label in doc.xpath("//label"):
                if label.attrib.get('for'):
                    if label.attrib['for'] == 'company_id':
                        parent = label.getparent()
                        parent.remove(label)
                    elif label.attrib['for'] == 'groups_id':
                        label.attrib['string'] = ''

            res['arch'] = etree.tostring(doc)
        return res