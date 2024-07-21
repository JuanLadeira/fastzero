from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Token
from fastzero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

T_Session = Annotated[Session, Depends(get_session)]
T_OauthForm= Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post('/token', response_model=Token)
def login(
    session: T_Session,
    form_data: T_OauthForm,
    ):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
        )
    if not user: 
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},   
        )
    
    if not verify_password(form_data.password, user.password):
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


@router.post('/refresh_token', response_model=Token)
def refresh_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={'sub': user.username})
    return {'access_token': new_access_token, 'token_type': 'bearer'}