import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

sys.path.append(".")

from api.config import DB_URI

engine = create_engine(DB_URI)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

Base = declarative_base()

def db_inject(func):
    def wrapper(*args, **kwargs):
        try:
            close = False
            if 'db' in kwargs and not isinstance(kwargs['db'], Session):
                raise Exception(
                    f"""Invalid argument db type passed to {func.__name__} required type: 
                    sqlalchemy.orm.session.Session - passed type: {type(kwargs['db'])}""")

            else:
                kwargs['db'] = db = SessionLocal()
                close = True

            return func(*args, **kwargs)
        finally:
            try:
                if close:
                    db.close()
            except Exception:
                pass
    return wrapper


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
