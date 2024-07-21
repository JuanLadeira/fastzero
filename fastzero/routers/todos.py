
# from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import Todo, User
from fastzero.schemas import TodoPublic, TodoSchema
from fastzero.security import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', response_model=TodoPublic)
def create_todos(
    session: T_Session,
    user: T_CurrentUser,
    todo: TodoSchema,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

 

# @router.get("/",response_model=TodosList)
# def read_todos():
#     ...


# @router.put('/{todo_id}', response_model=Todosublic)
# def update_todos(
#     ):
#    ...
# @router.delete(
#     '/{todo_id}',
#     response_model=Todo,
# )
# def delete_Todos():
#     ... 