from sqlalchemy import create_engine
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









