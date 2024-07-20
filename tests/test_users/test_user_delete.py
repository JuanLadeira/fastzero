from fastzero.schemas import UserPublic

def test_delete_user_without_user(client):
    response = client.delete('/users/1')
    assert response.status_code == 404


def test_read_users_with_user(client, user):

    response = client.delete(f'/users/{user.id}')

    assert response.status_code == 200
