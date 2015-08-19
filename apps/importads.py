# -*- coding: utf-8 -*-
# @filename importads
# @author   v-shijch
# @date     2015-08-18 14:40 PM

from structs.ads import AdsRecord, AdsLogRecord
from structs.common import BaseDocument
from services.config_service import MongoConfig
import mongoengine
from mongoengine import Q

import logging

logger = logging.getLogger('adsdemo.importads.' + __name__)


def importAdsRecord(_file, _class):
    count = 0
    with open(_file) as f:
        content = f.readlines()
        for _line in content:
            count += 1
            _record = _class.parse_line(_line)
            _record.save()
            if count % 10000 == 0:
                print '%d items have been parsed' % count
                break
    print 'All %d items have been parsed' % count


def importRecordsByFile(_file, _class):
    count = 0
    _class.objects.timeout(False)
    for _record in _class.parse_file(_file):
        _record.save()
        count += 1
        if count % 10000 == 0:
            print '%d items have been parsed' % count
            break
    print 'All %d items have been parsed' % count


if __name__ == '__main__':
    db = mongoengine.connect('ads_demo',
                             host=MongoConfig.url,
                             port=MongoConfig.port,
                             username=MongoConfig.user,
                             password=MongoConfig.password)

    # ads_corpus = r'D:\projects\Ads\DataPrepareForProj\AdsCorpus0809_900K_WithCampaignId.txt'
    # ads_log = r'D:\projects\Ads\DataPrepareForProj\AdsLog_1Month_Bing.txt'
    ads_corpus = r'D:/projects/Ads/DataPrepareForProj/AdsCorpus_100.txt'
    ads_log = r'D:/projects/Ads/DataPrepareForProj/AdsLog_100.txt'

    importAdsRecord(ads_corpus, AdsRecord)
    importAdsRecord(ads_log, AdsLogRecord)

    # importRecordsByFile(ads_corpus, AdsRecord)

    print 'done.'
