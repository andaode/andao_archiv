
# -*- coding: utf-8 -*-
from openerp import osv, models, fields, api, tools, _
import base64
import datetime
import logging
#import tesseract

#import cv2.cv as cv
_logger = logging.getLogger(__name__)





class Document(models.Model):
    _name = 'ocr.document'
    _inherit = 'mail.thread'
    _description = 'Archive document'

    name = fields.Char(string='Dokument ID')
    doc_name = fields.Char(string='Dokument')
    file_upload = fields.Binary(string='Datei', attachment=True)
    image_small = fields.Binary(string='Bild', attachment=True, readonly=True)
    image_medium = fields.Binary(string='Bild', attachment=True, readonly=True)
    image_big = fields.Binary(string='Bild', attachment=True, readonly=True)

    doc_text = fields.Text()
    owner = fields.Many2one('res.users', ondelete='set null', string="User")
    scanned_on = fields.Date(string='Gescannt am')
    received_on = fields.Date(string='Erhalten am')
    is_not_read = fields.Boolean()
    reminder = fields.Date()

    state = fields.Selection([('terminated', 'Verschoben'),('open', 'Nicht gelesen'), ('closed', 'Gelesen'), ('not_approved', 'Nicht bestätigt')
                              ], 'Status')
    def _resize_image(self):
        self.image = tools.image_resize_image_medium(self.image)

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
        self.state = 'open'

    @api.model
    def create(self, vals):
        self.env.cr.execute('SELECT count(name) FROM ocr_document WHERE owner = %s', (vals['owner'],))
        amount = str(self.env.cr.fetchall()[0][0] or 0)
        new_number = int(amount) + 1
        vals['name'] = 'Dokumen ' + str(new_number)
        vals['image_small'] = tools.image_resize_image_medium(vals['file_upload'])
        vals['image_medium'] = tools.image_resize_image_small(vals['file_upload'])
        vals['image_big'] = tools.image_resize_image_big(vals['file_upload'])
        vals['is_not_read'] = True
        if not vals['scanned_on'] :
            vals['scanned_on'] = str(datetime.datetime.now())[:10]
        if not vals['received_on']:
            vals['received_on'] = str(datetime.datetime.now())[:10]

        vals['image_big'] = tools.image_resize_image_big(vals['file_upload'])
        vals['state'] = 'not_approved'
        #self.ocr_file(file)
        if not vals['doc_name']:
            vals['doc_name'] = 'Dokument ' + str(new_number)
        agr = super(Document, self).create(vals)
        return agr

    # def ocr_file(self, file):
    #     mImgFile = "/Users/andrzej/projects/Octomore/ocr/data/0002AA72.jpg"
    #     api = tesseract.TessBaseAPI()
    #     api.SetOutputName("outputName");
    #     api.Init(".","eng",tesseract.OEM_DEFAULT)
    #     api.SetPageSegMode(tesseract.PSM_AUTO)
    #     #mImgFile = "eurotext.jpg"
    #     pixImage=cv.LoadImage(mImgFile)
    #     tesseract.SetCvImage(pixImage, api)
    #     outText=api.GetUTF8Text()
    #     print("OCR output:\n%s"%outText);
    #     api.End()