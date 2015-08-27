from handlers.foo import FooHandler
from handlers.test import TestHandler, TestHandler2, FakeAdsServeHandler

url_patterns = [
    (r"/foo", FooHandler),
    (r"/test1", TestHandler),
    (r"/test2", TestHandler2),
    (r"/random_ads", FakeAdsServeHandler)
]
