def test_user_delete_without_user(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == 403


def test_user_delete_with_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == 200
