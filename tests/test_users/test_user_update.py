def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': 'password1235!',
        }
    )
    assert response.status_code == 200
    assert response.json()['username'] == 'bob'
    assert response.json()['email'] == 'bob@gmail.com'
    

def test_update_user_excepetion(client):
    response = client.put(
        '/users/-1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 404
