# -*- coding: utf-8 -*-
# @filename config_service
# @author   v-shijch
# @date     2015-08-18 18:38 PM

class MongoConfig:
    url = '127.0.0.1'
    port = 30112
    user = 'mongoadmin'
    password = 'ads_microsoft'

class AdsQueryConfig:
    MinimumReturnRecordCount = 10
    Processors = [
        'http://127.0.0.1:3451/adstest'
    ]