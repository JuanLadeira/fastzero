
# from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends , Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from fastzero.database import get_session
from fastzero.models import Todo, User
from fastzero.schemas import TodoPublic, TodoSchema, TodoList
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

 

@router.get("/",response_model=TodoList)
def read_todos(
    session: T_Session,
    user: T_CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}
...


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