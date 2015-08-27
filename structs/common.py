# -*- coding: utf-8 -*-
# @filename common
# @author   v-shijch
# @date     2015-08-18 17:51 PM

from datetime import datetime

from mongoengine import Document
import random

class AdResponse():
    def __init__(self, _listing_id, _ad_id, _score):
        self.listingId = _listing_id
        self.adId = _ad_id
        self.score = _score

    def format(self):
        _data = {'ListingId':self.listingId, 'AdId':self.adId, 'score':self.score}
        return _data


class BaseDocument(Document):
    meta = {
        'abstract': True
    }

    @staticmethod
    def parse_line(_line):
        pass

    @classmethod
    def parse_file(_cls, _file):
        with open(_file) as f:
            content = f.readlines()
            for _line in content:
                yield _cls.parse_line(_line)