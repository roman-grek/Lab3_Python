import pytest
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from django.urls import reverse
from django.test import RequestFactory
from ..views import *
from ..models import TodoTable, TodoItem, Category


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user(request, db):
    return mixer.blend(User, username=request.param)


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_table_list(factory, user):
    path = reverse('tasks:list')
    request = factory.get(path)
    request.user = user
    view = TaskListView.as_view()
    response = view(request)
    assert response.status_code == 200

    request.user = AnonymousUser()
    response = view(request)
    assert response.status_code == 302


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_table_by_id(factory, user):
    TodoTable.objects.create(owner=user, id=1)
    path = reverse('tasks:table', kwargs={'uid': 1})
    request = factory.get(path)
    request.user = user
    response = table_by_id(request, 1)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_create_table(factory, user):
    path = reverse('tasks:create-table')
    request = factory.get(path)
    request.user = user
    view = TaskCreateTableView.as_view()
    response = view(request)
    assert response.status_code == 200

    category = Category.objects.create()
    request_post = factory.post(path, {'title': 'title', 'category': category}, follow=True)
    request_post.user = user
    response = view(request_post)
    assert response.status_code == 302


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_create_task(factory, user):
    path = reverse('tasks:create')
    request = factory.get(path)
    request.user = user
    view = TaskCreateView.as_view()
    response = view(request)
    assert response.status_code == 200

    request_post = factory.post(path, {'description': 'test'}, follow=True)
    request_post.user = user
    response = view(request_post)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_task_details(factory, user):
    table = mixer.blend(TodoTable, owner=user)
    mixer.blend(TodoItem, id=1, table=table)
    request = factory.get(reverse('tasks:details', kwargs={'pk': 1}))
    request.user = user
    view = TaskDetailsView.as_view()
    response = view(request, pk=1)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_task_complete(factory, user):
    table = mixer.blend(TodoTable, owner=user)
    mixer.blend(TodoItem, id=1, table=table)
    request = factory.get(reverse('tasks:complete', kwargs={'uid': 1}))
    request.user = user
    response = complete_task(request, 1)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_task_delete(factory, user):
    table = mixer.blend(TodoTable, owner=user)
    mixer.blend(TodoItem, id=1, table=table)
    request = factory.get(reverse('tasks:delete', kwargs={'uid': 1}))
    request.user = user
    response = delete_task(request, 1)
    assert response.status_code == 302


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_table_delete(factory, user):
    mixer.blend(TodoTable, owner=user, id=1)
    request = factory.get(reverse('tasks:delete-table', kwargs={'uid': 1}))
    request.user = user
    response = delete_table(request, 1)
    assert response.status_code == 302


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_comment_delete(factory, user):
    table = mixer.blend(TodoTable, owner=user)
    mixer.blend(Comment, table=table, text='text', id=1)
    request = factory.get(reverse('tasks:delete_comment', kwargs={'uid': 1}))
    request.user = user
    response = delete_comment(request, 1)
    assert response.status_code == 302


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_add_comment(factory, user):
    mixer.blend(TodoTable, owner=user, id=1)
    path = reverse('tasks:add_comment', kwargs={'uid': 1})
    request_post = factory.post(path, {'text': 'text'}, follow=True)
    request_post.user = user
    response = add_comment(request_post, 1)
    assert response.status_code == 302

    request = factory.get(path)
    request.user = user
    response = add_comment(request, 1)
    assert response.status_code == 200
