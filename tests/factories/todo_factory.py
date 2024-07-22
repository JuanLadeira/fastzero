import factory
import factory.fuzzy

from fastzero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Sequence(lambda n: f'todo{n}')
    description = factory.LazyAttribute(lambda obj: f'{obj.title} description')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


    