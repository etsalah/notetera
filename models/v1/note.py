from datetime import datetime
from models.v1.base import Base, model_to_dict
from sqlalchemy import Column, String, UnicodeText, ForeignKey, DateTime


class Note(Base):
    __tablename__ = 'note'
    id = Column('id', String(100), primary_key=True)
    content = Column('content', UnicodeText())
    created_at = Column(
        'created_at', DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        'updated_at', DateTime, onupdate=datetime.utcnow
    )
    deleted_at = Column('deleted_at', DateTime)
    created_by_id = Column(
        'created_by_id', String(100), ForeignKey('users.id'), nullable=False)
    ver = Column('ver', String(100), nullable=False)

    COLUMNS = (
        'id', 'content', 'created_at', 'updated_at', 'deleted_at', 'ver',
        'created_by_id'
    )

    def dict(self):
        return model_to_dict(self, Note.COLUMNS)
