# Methods for database connection and interaction with models.

from .db_config import DBConfig

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)


db_config = DBConfig()
connection_string = db_config.connection_string

async_engine = create_async_engine(url=connection_string)
async_session_maker = async_sessionmaker(bind=async_engine,
                                         class_=AsyncSession,
                                         expire_on_commit=False)


def connection(calb):
    """ Wrapper that creates a session and executes a callable with a session argument.
    """
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await calb(*args, session=session, **kwargs)
            except Exception as exc:
                await session.rollback()
                raise exc
            finally:
                await session.close()
    return wrapper
