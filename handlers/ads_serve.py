#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  ads_serve
# @author   dectinc@icloud.com
# @date     2015-08-27 23:49

import json
import urllib2
import random

from mongoengine import Q

from handlers.base import BaseHandler
from settings import get_template
from structs.ads import AdsRecord
from structs.common import AdResponse


class Processor():
    def __init__(self, name, url, index, weight=1, enable=True, show=True, description=None):
        self.name = name
        self.url = url
        self.idx = index
        self.weight = weight
        self.enable = enable
        self.show = show
        self.description = description


PROCESSORS = [
    Processor('Basic EM+PM', 'http://10.172.132.133:12306', 1, description='Basic EM+PM matching'),
    Processor('nGram matching', 'http://10.172.117.17:8080/', 2),
    Processor('Normalizer based matching', 'http://10.172.132.133:12306', 3, show=False),
    Processor('IR based matching', 'http://10.172.116.209:9595', 4),
    Processor('Directly table look up', 'http://172.23.149.227:8080/adServer/', 5),
]


def get_random_ads(_minN):
    _results = []
    _ads = AdsRecord.objects().skip(random.randint(0, 100)).limit(_minN)
    for _ad in _ads:
        assert isinstance(_ad, AdsRecord)
        _response = AdResponse(_ad.ListingId, _ad.AdId, random.random())
        _results.append(_response.format())
    _results = sorted(_results, key=lambda _result: _result['score'], reverse=True)
    return _results


def collect_results(_results):
    ads = {}
    for _processor in PROCESSORS:
        if not _processor.enable:
            continue
        for _ad in _results[_processor.name]:
            _key = (_ad['ListingId'], _ad['AdId'])
            ads[_key] = ads.get(_key, 0) + _ad['score']
    _top_results = sorted(ads, key=ads.get, reverse=True)
    # _top_results = sorted(ads.items(), key=operator.itemgetter(1), reverse=True)
    return len(ads), _top_results[0:10]


class FakeAdsServeHandler(BaseHandler):
    def post(self):
        _query, _minN = self.get_arguments('query', 'minN')
        print _query
        _results = get_random_ads(_minN)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(json.dumps(_results))


class AdServeHandler(BaseHandler):
    cache = {}

    def get(self):
        _param = self.request.arguments
        if _param is None or len(_param) == 0:
            self.render(get_template('portal_bing.html'))
        else:
            query = self.get_argument("q")
            enabled_processors = self.get_argument("p")

            def get_ads(processor, minN=10, debug=True):
                if debug:
                    response = get_random_ads(minN)
                else:
                    _params = {'query': query, 'minN': minN}
                    req = urllib2.Request(processor.url)
                    req.add_header('Content-Type', 'application/json')
                    response = urllib2.urlopen(req, json.dumps(_params))
                return response

            def checked(processor):
                return 'checked=checked' if processor.enable else ''


            if query in AdServeHandler.cache:
                results = AdServeHandler.cache.get(query)
            else:

                # pool = ThreadPool(6)
                # _results = {}
                # for _processor in PROCESSORS:
                # _results[_processor.name] = pool.apply_async(get_ads, PROCESSORS)
                # results = {_key:_results[_key].get() for _key in _results}

                results = {_processor.name: get_ads(_processor) for _processor in PROCESSORS}
                AdServeHandler.cache[query] = results

            for _processor in PROCESSORS:
                if str(_processor.idx) in enabled_processors:
                    _processor.enable = True
                else:
                    _processor.enable = False
            num_results, top10_results = collect_results(results)

            render_results = []
            for listingId, adId in top10_results:
                _ad = AdsRecord.objects(Q(ListingId=listingId) & Q(AdId=adId)).first()
                if _ad is None:
                    continue
                render_results.append(_ad)
                # render_results.append(_ad.to_render(query))
            _processors_shown = filter(lambda _processor: _processor.show, PROCESSORS)
            self.render(get_template('search_bing.html'), num_results=num_results,
                        result=render_results, query=query, processors=_processors_shown,
                        checked=checked)