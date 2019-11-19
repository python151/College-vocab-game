import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool

Base = declarative_base()

class Log(Base):
    __tablename__ = 'log' 
    id = Column(Integer, primary_key=True)
    endpoint = Column(String(250), nullable=False)
    ip = Column(String(250), nullable=False) 

# this is the engine it is being run on the SingletonThreadPool to maintain thread 
engine = create_engine('sqlite:///database.db', poolclass=SingletonThreadPool)
Base.metadata.create_all(engine)