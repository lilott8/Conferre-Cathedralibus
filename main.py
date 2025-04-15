import logging
import sys
from argparse import Namespace, ArgumentParser
import colorlog
import os
from config import Config
from utils.migration import run_migration
import asyncio

logger = colorlog.getLogger("main")


async def main(args: Namespace):
    logger.info(args.working_dir)
    config = Config(args)
    logger.info(config)
    await init(config)


async def init(config: Config):
    run_migration(config.db)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    colorlog.basicConfig(level=logging.DEBUG,
                         format='%(log_color)s%(levelname)s:\t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s')
    parser = ArgumentParser()
    default_path = os.path.expanduser("~/")
    parser.add_argument('-c', '--config', required=True, help="Path to config")
    parser.add_argument('-wd', '--working_dir', default=default_path, help="Temporary working directory")

    asyncio.run(main(parser.parse_args(sys.argv[1:])))
