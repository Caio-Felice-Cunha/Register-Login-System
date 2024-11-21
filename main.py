from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from models import *
from secrets import token_hex

app = FastAPI()


def connectDB():
    engine = create_engine(CONN, echo = True)
    Session = sessionmaker(bind = engine)
    return Session()

@app.post('/register')
def register(name: str, user: str, passwd: str):
    session = connectDB()
    existing_user = session.query(Person).filter_by(user=user, passwd=passwd).all()
    if len(existing_user) == 0:
        x = Person(name=name, user=user, passwd=passwd)
        session.add(x)
        session.commit()
        return {'status': 'success'}
    elif len(existing_user) > 0:
        return {'status': 'User already registered'}


