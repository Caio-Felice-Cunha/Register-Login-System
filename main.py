from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

USER = 'ROOT'
PASSWD = ''
HOST = 'localhost'
DATABASE = 'userDB'
PORT = '3306'

CONN = f"mysql+pymysql://{USER}:{PASSWD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Person(Base):
    __tablename__ = 'Person'
    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    user = Column(String(20))
    passwd = Column(String(10))







