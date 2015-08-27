import logging
import tornado
import tornado.template
import os
from tornado.options import define, options

import environment
import logconfig
import sys

from services.config_service import MongoConfig, MongoConfigMac
import mongoengine

reload(sys)
sys.setdefaultencoding('utf-8')

# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
tornado.options.parse_command_line()

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

def get_template(_name):
    assert isinstance(_name, str)
    return path(TEMPLATE_ROOT, _name)

# Deployment Configuration

class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }


if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = MEDIA_ROOT
settings['cookie_secret'] = "dectinc@microsoft:ads"
settings['xsrf_cookies'] = False
# settings['xsrf_cookies'] = True
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

_config = MongoConfigMac()
# _config = MongoConfig()
db = mongoengine.connect('ads_demo',
                         host=_config.url,
                         port=_config.port,
                         username=_config.user,
                         password=_config.password)
settings['db'] = db

SYSLOG_TAG = "boilerplate"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
    'loggers': {
        'boilerplate': {},
        'adsdemo.importads': {
            'handlers': ['file', 'console']
        }
    },
}

if settings['debug']:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

logconfig.initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
                             LOG_LEVEL, USE_SYSLOG)

if options.config:
    tornado.options.parse_config_file(options.config)