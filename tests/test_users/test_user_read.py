def test_read_users_whitout_users(client):
    response = client.get(
        '/users/',
    )
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    response = client.get(
        '/users/',
    )
    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'juan', 
                'email': 'juan@gmail.com'
            }
        ]
    }  


def test_read_user_not_found(client):
    response = client.get(
        '/users/1',
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client, user):
    response = client.get(
        '/users/1',
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'juan',
        'email': 'juan@gmail.com'
        }