import factory

from fastzero.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}!')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@gmail.com')