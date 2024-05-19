import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from .config import user, password, host, db_name

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return
    conn_str = f'postgresql+psycopg2://{user}:{password}@{host}/{db_name}'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
