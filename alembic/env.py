from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import colorlog

from models import BaseModel

# Alembic Config object
alembic_config = context.config

# Setup logging
fileConfig(alembic_config.config_file_name)

# Inject DB URL from HOCON config
# alembic_config.set_main_option('sqlalchemy.url', config['database']['url'])
target_metadata = BaseModel.metadata


def run_migrations_offline():
    """Run migrations without DB connection."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations with DB connection."""
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
