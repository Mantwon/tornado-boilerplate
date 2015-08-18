# -*- coding: utf-8 -*-
# @filename common
# @author   v-shijch
# @date     2015-08-18 17:51 PM

from datetime import datetime

from mongoengine import Document


class BaseDocument(Document):
    meta = {
        'abstract': True
    }
