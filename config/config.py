import colorlog
from argparse import Namespace
from pyhocon import ConfigFactory
from .database import Database
from .scraper import Scraper


class Config(object):

    def __init__(self, args: Namespace):
        self.log = colorlog.getLogger(self.__class__.__name__)
        self.args = args
        self.working_dir = args.working_dir

        conf = ConfigFactory.parse_file(args.config)
        self.db = Database(conf.get("db"))
        self.scraper = Scraper(conf.get("crawler"))

    def __repr__(self):
        return f"Database: {self.db}\t Scraper: {self.scraper}"
