def test_users_list_whitout_users(client):
    response = client.get(
        '/users/',
    )
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_users_list_with_users(client, user):
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

def test_users_list_limit_1(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Dante', 
            'email': 'dante@gmail.com',
            'password': '12352524$%!45',
        }
    )
    assert response.status_code == 201
    
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
