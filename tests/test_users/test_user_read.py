def test_user_read_not_found(client):
    response = client.get(
        '/users/1',
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_user_read (client, user):
    response = client.get(
        '/users/1',
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'juan',
        'email': 'juan@gmail.com'
        }