from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
#import datetime
from datetime import datetime, timezone

USER = 'root'
PASSWD = ''
HOST = 'localhost'
DATABASE = 'userDB'
PORT = '3306'

#CONN = f"sqlite+pymysql://{USER}:{PASSWD}@{HOST}:{PORT}/{DATABASE}"
CONN = f"sqlite:///{DATABASE}.db"


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

class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(Integer, primary_key = True)
    id_person = Column(Integer, ForeignKey('Person.id'))
    token = Column(String(100))
    #date = Column(DateTime, default = datetime.datetime.utcnow())
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(engine)






