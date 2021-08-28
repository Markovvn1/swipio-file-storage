from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

SQLBase = declarative_base()


class User(SQLBase):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    pass_sha256 = Column(String(64))


class File(SQLBase):
    __tablename__ = 'file'
    file_uid = Column(String(32), primary_key=True)
    file_sha256 = Column(String(64))
    file_path = Column(String(255))
    file_original_name = Column(String)
    file_media_type = Column(String)
