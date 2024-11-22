from tokenize import Token
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


@app.post('/login')
def login(user: str, passwd: str):
    session = connectDB()
    users = session.query(Person).filter_by(user = user, passwd = passwd).all()

    if len(users) == 0:
        return {'status': 'user not registered' } 

    while True:
        token = token_hex(50)
        existingToken = session.query(Tokens).filter_by(token=token).all()

        if len(existingToken) == 0:
            existingPerson = session.query(Tokens).filter_by(id_person = users[0].id).all()
            
            if len(existingPerson) == 0:
                newToken = Tokens(id_person = users[0].id, token=token)
                session.add(newToken)

            elif len(existingPerson) > 0:
                existingPerson[0].token = token

            session.commit()
            break

    return token

            
            




