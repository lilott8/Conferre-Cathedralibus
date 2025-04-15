import os
from alembic import command
from alembic.config import Config
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists, create_database

from config import Database
import colorlog


logger = colorlog.getLogger("migration")


def run_migration(db: Database):
    create_db(db)
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../alembic.ini'))
    alembic_cfg.set_main_option('script_location', os.path.join(os.path.dirname(__file__), '../alembic'))
    alembic_cfg.set_main_option('sqlalchemy.url', db.get_db_url_sync())

    command.upgrade(alembic_cfg, "head")


def create_db(db: Database):
    engine = create_engine(db.get_db_url_sync())
    logger.info(engine.url)
    if not database_exists(engine.url):
        logger.info(f"Creating database: {db.db_name}")
        create_database(engine.url)
    else:
        logger.debug(f"Database {db.db_name} already exists")
