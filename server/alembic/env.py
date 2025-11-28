from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import MetaData
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from database.database import Base  # your declarative base
import asyncio
from database.models import Base
from database.models import User
target_metadata=Base.metadata
import os
# this is the Alembic Config object
config = context.config
DATABASE_URL = os.environ.get("DATABASE_URL")
# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

target_metadata = Base.metadata  # use your models

# Async run migrations
def run_migrations_online():
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations_sync)

    def do_run_migrations_sync(connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations())

run_migrations_online()
