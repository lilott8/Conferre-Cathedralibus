import colorlog

from config import Config


class Crawler(object):

    def __init__(self, config: Config):
        self.logger = colorlog.getLogger(Crawler.__name__)
        self.config = config
        pass