
# -*- coding: utf-8 -*-
from openerp import osv, models, fields, api, tools, _
import base64
import datetime
import logging
import tesseract

#import cv2.cv as cv
_logger = logging.getLogger(__name__)





class Document(models.Model):
    _name = 'ocr.document'
    _inherit = 'mail.thread'
    _description = 'Archive document'

    def _get_name(self):
        self.env.cr.execute('SELECT count(name) FROM ocr_document WHERE owner = %s', (self.owner.id,))
        self.computed_rentable_area = str(self.env.cr.fetchall()[0][0] or 0)
        return datetime.date(2005, 1, 1)

    name = fields.Char(string='Document ID')
    doc_name = fields.Char(string='Document')
    file_upload = fields.Binary('File', attachment=True, readonly=True)
    image_small = fields.Binary('Image', attachment=True, readonly=True)
    image_medium = fields.Binary('Image', attachment=True, readonly=True)
    image_big = fields.Binary('Image', attachment=True, readonly=True)

    doc_text = fields.Text()
    owner = fields.Many2one('res.users', ondelete='set null', string="User")
    scanned_on = fields.Date()
    received_on = fields.Date()
    is_not_read = fields.Boolean()
    reminder = fields.Date()

    def _resize_image(self):
        self.image = tools.image_resize_image_medium(self.image)


############
    # _columns = {
    # 'name': fields.char('Name', required=True, translate=True),
    # 'image': fields.binary("Image",
    #         help="This field holds the image used as image for our customers, limited to 1024x1024px."),
    # 'image_medium': fields.function('_get_image', fnct_inv='_set_image',
    #         string="Image (auto-resized to 128x128):", type="binary", multi="_get_image",
    #         store={
    #             'upload_images.tutorial': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
    #         },help="Medium-sized image of the category. It is automatically "\
    #              "resized as a 128x128px image, with aspect ratio preserved. "\
    #              "Use this field in form views or some kanban views."),
    # 'image_small': fields.function('_get_image', fnct_inv='_set_image',
    #         string="Image (auto-resized to 64x64):", type="binary", multi="_get_image",
    #         store={
    #             'upload_images.tutorial': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
    #         },
    #         help="Small-sized image of the category. It is automatically "\
    #              "resized as a 64x64px image, with aspect ratio preserved. "\
    #              "Use this field anywhere a small image is required."),
    # }

    # def _get_image(self, cr, uid, ids, name, args, context=None):
    #     result = dict.fromkeys(ids, False)
    #     for obj in self.browse(cr, uid, ids, context=context):
    #         result[obj.id] = tools.image_get_resized_images(obj.image)
    #     return result
    #
    # def _set_image(self, cr, uid, id, name, value, args, context=None):
    #     return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
############



    @api.multi
    def make_is_read(self):
        self.ensure_one()
        self.is_not_read = not self.is_not_read

    @api.model
    def create(self, vals):
        self.env.cr.execute('SELECT count(name) FROM ocr_document WHERE owner = %s', (vals['owner'],))
        amount = str(self.env.cr.fetchall()[0][0] or 0)
        new_number = int(amount) + 1
        vals['name'] = 'Document ' + str(new_number)
        vals['image_small'] = tools.image_resize_image_medium(vals['file_upload'])
        vals['image_medium'] = tools.image_resize_image_small(vals['file_upload'])
        vals['image_big'] = tools.image_resize_image_big(vals['file_upload'])
        vals['is_not_read'] = True
        if not vals['scanned_on'] :
            vals['scanned_on'] = str(datetime.datetime.now())[:10]
        if not vals['received_on'] :
            vals['received_on'] = str(datetime.datetime.now())[:10]

        vals['image_big'] = tools.image_resize_image_big(vals['file_upload'])
        #self.ocr_file(file)
        if not vals['doc_name']:
            vals['doc_name'] = 'Document ' + str(new_number)
        agr = super(Document, self).create(vals)
        return agr

    def ocr_file(self, file):
        mImgFile = "/Users/andrzej/projects/Octomore/ocr/data/0002AA72.jpg"
        api = tesseract.TessBaseAPI()
        api.SetOutputName("outputName");
        api.Init(".","eng",tesseract.OEM_DEFAULT)
        api.SetPageSegMode(tesseract.PSM_AUTO)
        #mImgFile = "eurotext.jpg"
        pixImage=cv.LoadImage(mImgFile)
        tesseract.SetCvImage(pixImage, api)
        outText=api.GetUTF8Text()
        print("OCR output:\n%s"%outText);
        api.End()