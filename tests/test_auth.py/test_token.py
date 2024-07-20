def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password}
    )
    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token
    assert token["token_type"] == "bearer"