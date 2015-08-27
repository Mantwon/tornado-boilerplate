#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  test.py
# @author   dectinc@icloud.com
# @date     2015-08-24 23:15

import random

from handlers.base import BaseHandler
from structs.common import AdResponse
from structs.ads import AdsRecord
import json

class FakeAdsServeHandler(BaseHandler):
    def post(self):
        _query, _minN = self.get_arguments('query', 'minN')
        print _query
        _results = []
        _ads = AdsRecord.objects().skip(random.randint(0, 100)).limit(_minN)
        for _ad in _ads:
            assert isinstance(_ad, AdsRecord)
            _response = AdResponse(_ad.ListingId, _ad.AdId, random.random())
            _results.append(_response.format())
        _results = sorted(_results, key=lambda _result:_result['score'])
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(json.dumps(_results))


class TestHandler(BaseHandler):
    def get(self):
        url = ''
        activity = ''
        try:
            url = self.get_argument("url")
            activity = self.get_arguments('activity')
        except:
            self.render('../templates/portal.html', url="", result=[])
            return
        print url
        print activity
        self.render('../templates/portal.html', url=url, result=activity)


class TestHandler2(BaseHandler):
    def get(self):
        print 'say hello'
        items = ["item1", "item2", "item3"]
        # render the corresponding template file, and pass the "**args" to the assigned template
        # not only we can pass the realted parameters, but also can pass the related functions.
        # so extendible and powerful! :)
        items2 = ["item1", "item2"]

        def checked(item):
            return 'checked=checked' if item in items2 else ''

        self.render("../templates/test1.html", items=items, add=add, items2=items2, checked=checked)


# define one "add" customization funcation which will be used in the assigned template file.
def add(x, y):
    return (x + y)