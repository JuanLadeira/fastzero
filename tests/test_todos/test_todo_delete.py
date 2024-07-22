from http import HTTPStatus


def test_delete_todo(session, client, user, token, todo_factory):
    todo = todo_factory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        'detail': 'Task has been deleted successfully.'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todos/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND, response.json()
    assert response.json() == {'detail': 'Task not found.'}