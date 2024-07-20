from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Message, Token, UserList, UserPublic, UserSchema
from fastzero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

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
    session: Session = Depends(get_session),
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
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
    ):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only update your own user'
        )
    
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user

@app.delete(
    '/users/{user_id}',
    response_model=Message,
)
def delete_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
    ):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only update your own user'
        )

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}


@app.post('/token', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
    ):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
        )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token({'sub': user.username})
    
    return {
        'access_token': access_token,
        'token_type': 'bearer'
        }