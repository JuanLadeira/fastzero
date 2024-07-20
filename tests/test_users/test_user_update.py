def test_user_update(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': 'password1235!',
        }
    )
    assert response.status_code == 200
    assert response.json()['username'] == 'bob'
    assert response.json()['email'] == 'bob@gmail.com'
    

def test_user_update_exception(client, token):
    response = client.put(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not enough permissions'}