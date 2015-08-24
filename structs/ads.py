# -*- coding: utf-8 -*-
# @filename ads
# @author   v-shijch
# @date     2015-08-18 17:53 PM

import logging

from mongoengine import StringField, IntField, FloatField, LongField, ListField

from common import BaseDocument


logger = logging.getLogger('adsdemo.ads')


class AdsRecord(BaseDocument):
    CampaignId = IntField(required=True)
    ListingId = LongField(required=True)
    AdId = LongField(required=True)
    BidKeyword = StringField()
    Matchtypes = ListField(StringField(), default=[])
    ExactBid = IntField()
    PhraseBid = IntField()
    BroadBid = IntField()
    ActualAdTitle = StringField()
    ActualAdDesc = StringField()
    ActualDisplayURL = StringField()
    ActualDestinationURL = StringField()
    MatchTypeId = IntField()

    meta = {
        'collection': 'ads_corpus',
        'indexes': [
            {
                'fields': [
                    'CampaignId',
                    'ListingId',
                    'AdId'
                ],
            }
        ],
        'index_background': True
    }

    @staticmethod
    def parse_line(_line):
        assert isinstance(_line, str) \
               and _line is not None \
               and len(_line) != 0
        _fields = _line.split('\t')
        if len(_fields) != 13:
            logger.error('not enough fields: %s' % _line)
        record = AdsRecord()
        record.CampaignId = int(_fields[0])
        record.ListingId = long(_fields[1])
        record.AdId = long(_fields[2])
        record.BidKeyword = _fields[3]
        record.Matchtypes = _fields[4].split(',')
        if _fields[5] is not None and len(_fields[5]) != 0:
            record.ExactBid = int(_fields[5])
        if _fields[6] is not None and len(_fields[6]) != 0:
            record.PhraseBid = int(_fields[6])
        if _fields[7] is not None and len(_fields[7]) != 0:
            record.BroadBid = int(_fields[7])
        record.ActualAdTitle = _fields[8]
        record.ActualAdDesc = _fields[9]
        record.ActualDisplayURL = _fields[10]
        record.ActualDestinationURL = _fields[11]
        record.MatchTypeId = int(_fields[12])
        return record
        # yield record
        # record.save()

    def __str__(self):
        return '%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\n' \
               % (self.CampaignId,
                  self.ListingId,
                  self.AdId,
                  self.BidKeyword,
                  ','.join(self.Matchtypes),
                  str(self.ExactBid) if 'ExactBid' in self._data else '',
                  str(self.PhraseBid) if 'PhraseBid' in self._data else '',
                  str(self.BroadBid) if 'BroadBid' in self._data else '',
                  self.ActualAdTitle,
                  self.ActualAdDesc,
                  self.ActualDisplayURL,
                  self.ActualDestinationURL,
                  self.MatchTypeId
        )


class AdsLogRecord(BaseDocument):
    RGUID = StringField(required=True, primary_key=True)
    CleansedQuery = StringField()
    CleansedKeyword = StringField()
    AdvertiserId = IntField()
    CampaignId = IntField()
    ListingId = LongField()
    AdId = LongField()
    ValidImpression = IntField()
    ValidClicks = IntField()
    Clicked = IntField()
    AmountChargedUSDMonthlyExchangeRt = FloatField()
    DIS_AdLayoutId = StringField()
    DIS_AdRelativePosition = StringField()
    AdInfoSource = IntField()
    AdInfoScore = IntField()
    MatchTypeId = IntField()

    meta = {
        'collection': 'ads_log',
        'indexes': [
            {
                'fields': [
                    'RGUID',
                    'AdId',
                    'ListingId'
                ],
            }
        ],
        'index_background': True
    }

    @staticmethod
    def parse_line(_line):
        assert isinstance(_line, str) \
               and _line is not None \
               and len(_line) != 0

        _fields = _line.split('\t')
        if len(_fields) != 16:
            logger.error('not enough fields: %s' % _line)
        record = AdsLogRecord()
        record.RGUID = _fields[0]
        record.CleansedQuery = _fields[1]
        record.CleansedKeyword = _fields[2]
        record.AdvertiserId = int(_fields[3])
        record.CampaignId = int(_fields[4])
        record.ListingId = long(_fields[5])
        record.AdId = long(_fields[6])
        record.ValidImpression = int(_fields[7])
        record.ValidClicks = int(_fields[8])
        record.Clicked = int(_fields[9])
        record.AmountChargedUSDMonthlyExchangeRt = float(_fields[10])
        record.DIS_AdLayoutId = _fields[11]
        record.DIS_AdRelativePosition = _fields[12]
        if _fields[13] is not None and len(_fields[13]) != 0:
            record.AdInfoSource = int(_fields[13])
        if _fields[14] is not None and len(_fields[14]) != 0:
            record.AdInfoScore = int(_fields[14])
        record.MatchTypeId = int(_fields[15])
        return record
        # yield record
        # record.save()
