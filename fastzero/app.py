from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Message, UserList, UserPublic, UserSchema
from fastzero.security import get_password_hash, verify_password, create_access_token

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    """
    Create a new user
    """

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
    hashed_password = get_password_hash(user.password)

    user = User(
        username=user.username, email=user.email, password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 5,
    offset:int = 0,
    session: Session = Depends(get_session)
    ):
    db_users = session.scalars(
        select(User).offset(offset).limit(limit)
        ).all()    
         
    return {'users': db_users}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(
    user_id: int, 
    session: Session = Depends(get_session)
    ):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, 
    session: Session = Depends(get_session)
    ):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.delete(
    '/users/{user_id}',
    response_model=Message,
)
def delete_user(
    user_id: int, 
    session: Session = Depends(get_session)
    ):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}


@app.post('/token')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
    ):
    user = session.scalar(select(User).where(User.username == form_data.username))
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    return {'access_token': create_access_token(form_data.username), 'token_type': 'bearer'}