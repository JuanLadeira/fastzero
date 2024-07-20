def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }

def test_create_user_com_username_ja_registrado(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'juan',
            'email': 'joao@gmail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 400

def test_create_user_com_email_ja_registrado(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'joao',
            'email': 'juan@gmail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 400
