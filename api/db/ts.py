import sqlalchemy
from sqlalchemy.dialects.postgresql import TSVECTOR


class TSVector(sqlalchemy.types.TypeDecorator):
    impl = TSVECTOR