# -*- coding: utf-8 -*-
# @filename mongo_api
# @author   v-shijch
# @date     2015-08-19 13:34 PM

from base import  BaseHandler
from structs.ads import AdsRecord
import logging

logger = logging.getLogger('adsdemo.api.' + __name__)

def getAdById(_id):
    try:


class GetAdHandler(BaseHandler):
    def get(self, _adId):
        try:
            _arguments = self.request.arguments

        except Exception, e:
            logger.error(str(e))
