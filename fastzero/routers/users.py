from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Message, UserList, UserPublic, UserSchema
from fastzero.security import get_current_user, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Session = Annotated[Session, Depends(get_session)]

@router.post('/', status_code=201, response_model=UserPublic)
def create_user(
    session: T_Session,
    user: UserSchema, 
    ):
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


@router.get("/",response_model=UserList)
def read_users(
    session:T_Session,
    limit: int = 5,
    offset:int = 0,
    ):
    db_users = session.scalars(
        select(User).offset(offset).limit(limit)
        ).all()    
         
    return {'users': db_users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(
    session: T_Session,
    user_id: int, 
    ):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    session: T_Session,
    current_user : T_CurrentUser,
    user_id: int, user: UserSchema, 
    ):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )
    
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user

@router.delete(
    '/{user_id}',
    response_model=Message,
)
def delete_user(
    session: T_Session,
    current_user:T_CurrentUser,
    user_id: int, 
     ):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}
