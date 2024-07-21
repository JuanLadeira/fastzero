from fastzero.schemas import UserPublic


def test_users_list_whitout_users(client):
    response = client.get(
        '/users/',
    )
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_users_list_with_users(client, user, other_user):
    
    user_schema = UserPublic.model_validate(user).model_dump()
    other_user_schema = UserPublic.model_validate(other_user).model_dump()

    response = client.get(
        '/users/',
    )
    assert response.status_code == 200
    assert response.json() == {
        'users': [user_schema, other_user_schema]
    }  

def test_users_list_limit_1(client, user, other_user):
    response = client.get(
        '/users/',
        params={'limit': 1}
    )
    assert response.status_code == 200
    assert len(response.json()["users"]) == 1 

    response = client.get(
        '/users/',
        params={'limit': 2}
    )
    assert response.status_code == 200
    assert len(response.json()["users"]) == 2
