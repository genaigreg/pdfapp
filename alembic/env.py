from dotenv import load_dotenv
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import your models' Base
from database import Base  # <-- Replace 'your_app.models' with the correct path to your Base

# Alembic Config object
config = context.config

import os
config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata to the Base's metadata
target_metadata = Base.metadata  # This tells Alembic which models to use for autogeneration

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

