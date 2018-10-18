from datetime import datetime
from models.v1.base import Base, model_to_dict
from sqlalchemy import Column, String, Unicode, Integer, UnicodeText, ForeignKey
from sqlalchemy import DateTime

class Label(Base):
    __tablename__ = 'label'
    id = Column('id', String(100), primary_key=True)
    name = Column('name', Unicode(200), nullable=False, unique=True)
    created_by_id = Column(
        'created_by_id', String(100), ForeignKey('users.id'), nullable=False)
    created_at = Column(
        'created_at', DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        'updated_at', DateTime, onupdate=datetime.utcnow
    )
    deleted_at = Column('deleted_at', DateTime)
    ver = Column('ver', String(100), nullable=False)

    COLUMNS = (
        'id', 'name', 'created_by_id', 'created_at', 'updated_at', 'deleted_at',
        'ver'
    )

    def dict(self):
        return model_to_dict(self, Label.COLUMNS)
