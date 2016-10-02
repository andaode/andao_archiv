
# -*- coding: utf-8 -*-
from openerp import osv, models, fields, api, tools, _
import base64
import datetime
import logging
from PIL import Image as ImagePil
from pytesser import *
import cStringIO as StringIO
from openerp.exceptions import ValidationError
from ocr_recognition import TextRecognition
import StringIO
_logger = logging.getLogger(__name__)





class Document(models.Model):
    _name = 'archive.document'
    _inherit = 'mail.thread'
    _description = 'Archive document'
    _order = 'scanned_on desc'
    name = fields.Char(string='Dokument ID')
    doc_name = fields.Char(string='Dokument')

    file_upload = fields.Binary(string='Datei', attachment=True)
    image_filename = fields.Char(string='Dateiname')
    image_small = fields.Binary(string='Bild', attachment=True, readonly=True)
    #image_medium = fields.Binary(string='Bild', attachment=True, readonly=True)
    image_big = fields.Binary(string='Bild', attachment=True, readonly=True)
    company_id = fields.Many2one('res.company', string="Unternehmen")
    doc_text = fields.Text()
    owner = fields.Many2one('res.users', ondelete='set null', string="User")
    scanned_on = fields.Date(string='Gescannt am')
    received_on = fields.Date(string='Erhalten am')
    is_not_read = fields.Boolean()
    reminder = fields.Date()

    state = fields.Selection([('terminated', 'Verschoben'),('open', 'Nicht gelesen'), ('closed', 'Gelesen'), ('not_approved', 'Nicht bestätigt')
                              ], 'Status')
    # def _resize_image(self):
    #     self.image = tools.image_resize_image_medium(self.image)

    @api.multi
    @api.depends('reminder')
    def _set_state_to_terminated(self):
        self.ensure_one()
        if self.reminder:
            self.state = 'terminated'
        else:
            self.state = 'closed'

    @api.multi
    def make_is_read(self):
        self.ensure_one()
        if self.state != 'open':
            self.state = 'open'
        elif self.state == 'open':
            self.state = 'closed'

    @api.multi
    def make_approved(self):
        self.ensure_one()
        if self.owner:
            if not self.doc_name:
                self.env.cr.execute('SELECT count(name) FROM archive_document WHERE owner = %s', (self.owner.id,))
                amount = str(self.env.cr.fetchall()[0][0] or 0)
                new_number = int(amount) + 1
                self.doc_name = 'Dokument ' + str(new_number)
            self.state = 'open'
            self.send_email(self.owner.email)
        else:
            raise ValidationError(_("Das Dokument muss einen Besitzer haben"))

    @api.model
    def create(self, vals):
        #image_stream = StringIO.StringIO(vals['file_upload'].decode('base64'))
        file_upload_decoded = vals['file_upload'].decode('base64')
        jpg_str = self.convert_to_jpg(file_upload_decoded)

        vals['file_upload'] = base64.b64encode(jpg_str)
        vals['image_small'] = tools.image_resize_image_medium(vals['file_upload'])
        vals['image_big'] = tools.image_resize_image_big(vals['file_upload'])

        vals['is_not_read'] = True
        if not vals['scanned_on']:
            vals['scanned_on'] = str(datetime.datetime.now())[:10]
        if not vals['received_on']:
            vals['received_on'] = str(datetime.datetime.now())[:10]
        vals['state'] = 'not_approved'
        vals['company_id'] = self.env.user.company_id.id

        ocr_obj = self.env['archive.ocr']
        ocr_text = ocr_obj.ocr_file(file_upload_decoded)
        owner = ocr_obj.find_owner(ocr_text.decode('utf-8'), self.env.user.company_id.id)
        if owner:
            vals['owner'] = owner

        vals['doc_text'] = ocr_text
        agr = super(Document, self).create(vals)
        return agr

    @api.model
    def send_email(self, email_to):
        values = {
                 'subject': 'Neues Dokument erhalten!',
                 'body_html': 'BEsuchen Sie bitte <h>www.andao.de/archive</h> um das Dokumen zu sehen',
                 'email_to': email_to,
                 'email_from': 'info@andao.de',
                }
        mail_obj = self.env['mail.mail']
        msg_id = mail_obj.create(values)
        if msg_id:
            mail_obj.send([msg_id])
        return True


    def convert_to_jpg(self, file_upload_decoded):
        image_stream = StringIO.StringIO(file_upload_decoded)
        im = ImagePil.open(image_stream)

        jpg_stream = StringIO.StringIO()
        im.save(jpg_stream, format="JPEG")
        jpg_str = ''

        for txt in jpg_stream.buflist:
            jpg_str += txt

        jpg_stream.close()
        return  jpg_str