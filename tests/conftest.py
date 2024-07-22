import pytest
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import User, table_registry
from fastzero.security import get_password_hash
from tests.factories.todo_factory import TodoFactory
from tests.factories.user_factory import UserFactory

register(UserFactory)
register(TodoFactory)

@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
        app.dependency_overrides.clear()

    app.dependency_overrides.clear()


@pytest.fixture()
def other_user(session, user_factory):
    user = user_factory.create()
    session.add(user)
    session.commit()
    session.refresh(user)

    yield user
    

@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = "testpassword"
    user = User( 
        username="juan",
        email="juan@gmail.com",
        password=get_password_hash(pwd)
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd

    yield user


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    login_response = response.json()
    print(login_response)
    return login_response['access_token']