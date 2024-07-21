from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.username, 'password': user.clean_password}
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token["token_type"] == "bearer"



def test_get_token_wrong_password(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.username, 'password': "wrong_password"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_token_wrong_email(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': "emailerrado@gmail.com",
              'password': user.clean_password
        }
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED



def test_token_expired(client, user):
    with freeze_time('2021-01-01 00:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.username, 'password': user.clean_password}
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time('2021-01-01 00:32:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'bob',
                'email': 'bob@gmail.com',
                'password': 'password12315!',
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Token has expired'}

