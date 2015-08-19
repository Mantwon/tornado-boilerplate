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

    @staticmethod
    def parse_line(_line):
        pass

    @classmethod
    def parse_file(_cls, _file):
        with open(_file) as f:
            content = f.readlines()
            for _line in content:
                yield _cls.parse_line(_line)