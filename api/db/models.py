import re
import sys
import json
from uuid import uuid4, UUID
from enum import Enum
from typing import List, Optional, Union

from sqlalchemy import JSON, Boolean, Column, DateTime, Computed
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text, asc, Index
from sqlalchemy.dialects.postgresql import UUID as sqlUUID
from sqlalchemy.sql import func
from sqlalchemy import types

sys.path.append(".")

from api.db.database import Base, Session as DB, db_inject
from api.db.ts import TSVector




class Doc(Base):
    __tablename__ = "documents"
    id = Column(sqlUUID(as_uuid=True), primary_key=True, index=True)
    text = Column(Text())
    
    ts_vector = Column(TSVector(), Computed("to_tsvector('english', title)", persisted=True))
    
    __table_args__ = (Index('ix_video_ts_vector', ts_vector, postgresql_using='gin'),)
    
    @staticmethod
    @db_inject
    def create_document(id: Optional[UUID], text: Optional[str], db: DB) -> UUID:
        if id is None:
            id = uuid4()
            
        if text is None:
            text = ""
            
        rec = Doc()
        rec.id = id
        rec.text = text
        
        db.add(rec)
        db.commit()
        
        return id
    
    @staticmethod
    @db_inject
    def fts(text: str, db: DB) -> List[UUID]:
        res = db.query(Doc).filter(Doc.ts_vector.match(text)).all()
        ret_val: List[UUID] = []
        for element in res:
            ret_val.append(element.id)
            
        return ret_val
            
            
        
    



