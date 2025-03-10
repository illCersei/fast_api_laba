from alembic import context
from sqlalchemy import engine_from_config
from app.db.session import engine  # 🔹 Импортируем готовый движок
from app.models.users import Base  # 🔹 Импортируем метаданные моделей

target_metadata = Base.metadata

def run_migrations_online():

    with engine.connect() as connection:  # Используем готовый движок
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():

    context.configure(url=str(engine.url), target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
