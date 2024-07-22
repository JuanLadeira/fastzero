
def test_list_todos_should_return_5_todos(
        session, client, user, token, todo_factory
        ):
    expected_todos = 5
    session.bulk_save_objects(todo_factory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token, todo_factory
):
    expected_todos = 2
    session.bulk_save_objects(todo_factory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos