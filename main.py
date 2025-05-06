import logging
import sys
from argparse import Namespace, ArgumentParser
import colorlog
import os
from config import Config
from crawler import Crawler
from utils.migration import run_migration
import asyncio

logger = colorlog.getLogger("main")


def main(args: Namespace):
    logger.info(args.working_dir)
    config = Config(args)
    logger.info(config)
    init(args, config)

    logger.info(args.worker)
    if args.worker == "crawler":
        logger.info(f"Running: {args.worker}")
        crawler = Crawler(config)
    else:
        logger.info(f"Running other: {args.worker}")


def init(args: Namespace, config: Config):
    if args.migrate:
        logger.info("Beginning running migrations")
        # run_migration(config.db)
        logger.info("Completed running migrations")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    colorlog.basicConfig(level=logging.DEBUG,
                         format='%(log_color)s%(levelname)s:\t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s')
    parser = ArgumentParser()
    default_path = os.path.expanduser("~/")
    parser.add_argument('-c', '--config', required=True, help="Path to config")
    parser.add_argument('-wd', '--working_dir', default=default_path, help="Temporary working directory")
    parser.add_argument('-w', '--worker', default="crawler", choices={"crawler", "processor"})
    parser.add_argument("-m", "--migrate", action="store_true", help="Run database migrations.")

    main(parser.parse_args(sys.argv[1:]))
