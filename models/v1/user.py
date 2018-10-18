from datetime import datetime
from models.v1.base import Base, model_to_dict
from sqlalchemy import String, Unicode, DateTime, Column
from sqlalchemy import UniqueConstraint

class User(Base):
    __tablename__ = 'users'
    id = Column('id', String(100), primary_key=True)
    username = Column('username', Unicode(200), nullable=False, unique=True)
    password = Column('password', Unicode(300), nullable=False)
    email = Column('email', Unicode(200), nullable=False, unique=True)
    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    deleted_at = Column('deleted_at', DateTime)
    updated_at = Column('updated_at', DateTime, onupdate=datetime.utcnow)
    ver = Column('ver', String(100), nullable=False)

    COLUMNS = (
        'id', 'username', 'password', 'email', 'created_at', 'deleted_at',
        'updated_at', 'ver'
    )

    def dict(self):
        return model_to_dict(self, User.COLUMNS)
