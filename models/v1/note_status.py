from datetime import datetime
from models.v1.base import Base, model_to_dict
from sqlalchemy import Column, String, Unicode, Integer, UnicodeText, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import DateTime

class NoteStatus(Base):
    __tablename__ = 'note_status'
    __table_args__ = (
    	UniqueConstraint('status_id', 'note_id', name='uniq_note_status'),
    )
    id = Column('id', String(100), primary_key=True)
    status_id = Column(
    	'status_id', String(100), ForeignKey('status.id'), nullable=False)
    note_id = Column(
    	'note_id', String(100), ForeignKey('note.id'), nullable=False)
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
        'id', 'status_id', 'note_id', 'created_by_id', 'created_at',
        'updated_at', 'deleted_at', 'ver'
    )

    def dict(self):
        return model_to_dict(self, NoteStatus.COLUMNS)
