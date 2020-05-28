from mixer.backend.django import mixer
from django.urls import reverse
import pytest
from ..models import TodoItem


@pytest.fixture
def category(request, db):
    return mixer.blend('tasks_manager.Category', slug=request.param)


@pytest.fixture
def table(request, db):
    return mixer.blend('tasks_manager.TodoTable', title=request.param)


@pytest.fixture
def task(request, db):
    return mixer.blend('tasks_manager.TodoItem', description=request.param)


@pytest.fixture
def comment(request, db):
    return mixer.blend('tasks_manager.Comment', text=request.param)


@pytest.mark.parametrize('comment', ['Comment 1'], indirect=True)
def test_comment(comment):
    assert comment.__str__() == 'Comment 1'


@pytest.mark.parametrize('table', ['TestTable'], indirect=True)
def test_table(table):
    assert table.__str__() == 'TestTable'


@pytest.mark.parametrize('category', ['study'], indirect=True)
def test_category(category):
    assert category.__str__() == 'study'


@pytest.mark.parametrize('table', ['TestTable'], indirect=True)
def test_task(table):
    task = TodoItem.objects.create(table=table, description='Do something', owner=table.owner)
    assert task.__str__() == 'do something'
    assert task.get_absolute_url() == reverse("tasks:details", kwargs={'pk': task.pk})
