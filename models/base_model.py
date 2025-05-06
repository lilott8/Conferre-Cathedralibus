from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

engine = create_async_engine("", echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


def get_engine(db_url: str, echo: bool = True):
    return create_async_engine(db_url, echo=echo)


def get_session_maker(db_url: str, engine=None) -> async_sessionmaker[AsyncSession]:
    if engine is None:
        engine = get_engine(db_url)
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


def get_session(engine=None):
    session_maker = get_session_maker(engine)
    return session_maker()
