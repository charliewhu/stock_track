from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def db_session_maker(DATABASE_URL: str = "sqlite:///src/api/sqlite.db"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )
    return session()
