#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  verifyads
# @author   dectinc@icloud.com
# @date     2015-08-24 21:25

from structs.ads import AdsRecord, AdsLogRecord
from structs.common import BaseDocument
from services.config_service import MongoConfig, MongoConfigMac
import mongoengine
from mongoengine import Q
import codecs

import logging
import settings
import sys

logger = logging.getLogger('adsdemo.verifyads')


def verifyAdsRecord(_file, _class):
    logger.info(sys._getframe().f_code.co_name + _class.__name__)
    tmp = open(_class.__name__ + '_verify.txt', 'wb')
    count = 0
    with open(_file) as f:
        content = f.readlines()
        for _line in content:
            count += 1
            _record = _class.parse_line(_line)
            _record_in = _class.objects(Q(AdId=_record.AdId) & Q(CampaignId=_record.CampaignId) & Q(
                ListingId=_record.ListingId)).first()
            if _record_in is None:
                tmp.write(_line)
            if count % 10000 == 0:
                break
    tmp.flush()
    tmp.close()
    logger.info('verify %s done' % _class.__name__)

if __name__ == '__main__':
    sys.getdefaultencoding()
    _config = MongoConfigMac()
    db = mongoengine.connect('ads_demo',
                             host=_config.url,
                             port=_config.port,
                             username=_config.user,
                             password=_config.password)

    ads_corpus = r'/Users/Dectinc/Workspace/data/DataPrepareForProj/AdsCorpus0809_900K_WithCampaignId.txt'
    ads_log = r'/Users/Dectinc/Workspace/data/DataPrepareForProj/AdsLog_1Month_Bing.txt'
    # ads_corpus = r'D:\projects\Ads\DataPrepareForProj\AdsCorpus0809_900K_WithCampaignId.txt'
    # ads_log = r'D:\projects\Ads\DataPrepareForProj\AdsLog_1Month_Bing.txt'
    # ads_corpus = r'D:/projects/Ads/DataPrepareForProj/AdsCorpus_100.txt'
    # ads_log = r'D:/projects/Ads/DataPrepareForProj/AdsLog_100.txt'

    verifyAdsRecord(ads_corpus, AdsRecord)
    verifyAdsRecord(ads_log, AdsLogRecord)

    # out = open('AdsRecord.txt', 'wb')
    # ads_records = AdsRecord.objects()
    # for _record in ads_records:
    #     try:
    #         out.write(str(_record))
    #     except:
    #         print unicode(str(_record).strip(codecs.BOM_UTF8), 'utf-8')
    # out.flush()
    # out.close()