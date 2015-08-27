# -*- coding: utf-8 -*-
# @filename importads
# @author   v-shijch
# @date     2015-08-18 14:40 PM

from structs.ads import AdsRecord, AdsLogRecord
from structs.common import BaseDocument
from services.config_service import MongoConfig, MongoConfigMac
import mongoengine
from settings import settings
from mongoengine import Q

import logging
import settings

logger = logging.getLogger('adsdemo.importads')

def importAdsRecord(_file, _class):
    logger.info('Get in: ' + _class.__name__)
    count = 0
    with open(_file) as f:
        content = f.readlines()
        for _line in content:
            count += 1
            _record = _class.parse_line(_line)
            _record_in = _class.objects(__raw__=_record._data).first()
            if _record_in is not None:
                logger.info('duplicate record: ' + _line)
                continue
            _record.save(force_inset=True, validate=False)
            if count % 1000 == 0:
                print '. ',
            if count % 10000 == 0:
                print '%d items have been parsed' % count
                break
    print 'All %d items have been parsed' % count
    # logger.info('All %d items have been parsed' % count)



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
    AdsRecord.drop_collection()
    AdsLogRecord.drop_collection()

    importAdsRecord(ads_corpus, AdsRecord)
    importAdsRecord(ads_log, AdsLogRecord)

    # importRecordsByFile(ads_corpus, AdsRecord)

    print 'done.'
