from fastzero.schemas import UserPublic

def test_read_users_without_user(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {"users": []}

def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {"users": [user_schema]}
