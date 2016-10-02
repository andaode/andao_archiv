
# -*- coding: utf-8 -*-
from openerp import osv, models, fields, api, tools, _
import base64
import datetime
import logging
from PIL import Image as ImagePil
from pytesser import *
import cStringIO as StringIO
from openerp.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class TextRecognition(models.Model):
    _name = 'archive.ocr'

    def ocr_file(self, file_upload_decoded):
        image_stream = StringIO.StringIO(file_upload_decoded)
        #im = dupa.open('/home/andy/' + file_name)
        im = ImagePil.open(image_stream)
        text = pytesser.image_to_string(im)
        return text


    @api.multi
    def find_owner(self, ocr_text, company_id):
        users = self.env['res.users'].search([('company_id', '=', company_id)])
        user_list = []
        for user in users:
            if user.name in ocr_text:
                if user.surname in ocr_text:
                    user_list.append(user)
                    # surname_position = ocr_text.find(user.name)
                    # search_begin = 0 if surname_position <= 50 else surname_position -50
                    # search_end = ocr_text.length if ocr_text.length - surname_position <= 50 else surname_position + 50
                    # ocr_text_surrunding_name = ocr_text[search_begin:search_end]
                    # if user.surname in ocr_text_surrunding_name:
                    #     user_list.append(user)
                    # else: user.surname in ocr_text:
                    #     # todo sprawdzic w okolicy paru znakow od nazwiska
                    #     user_list.append(user)

        if len(user_list) == 1:
            return user_list[0].id
        elif len(user_list) == 0:
            for user in users:
                if user.name in ocr_text:
                        user_list.append(user)
            if len(user_list) == 1:
                return user_list[0].id
            elif len(user_list) == 0:
                user_id = self.find_user_with_spelling_mistakes(users, ocr_text)
                return user_id
            else:
                return None
        else: #many users
            return None

    def find_user_with_spelling_mistakes(self, users, ocr_text):
        # todo nowy algorytm ze zmienianiem liter
        return None