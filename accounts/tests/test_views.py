import pytest
from mixer.backend.django import mixer
from django.urls import reverse
from django.test import RequestFactory
from ..views import *
from ..tokens import token_generator


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user(request, db):
    return mixer.blend(User, username=request.param)


@pytest.fixture
def profile(request, db):
    return mixer.blend(Profile, user=request.param)


def test_register(client, django_user_model):
    path = reverse('register')
    response = client.get(path)
    assert response.status_code == 200

    response = client.post(path, {'username': 'admin', 'first_name': 'roman', 'last_name': 'grek',
                                  'email': 'roman.grek@gmail.com', 'password': 'lahsdflk344',
                                  'password2': 'lahsdflk344'}, follow=True)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_edit_view(factory, user):
    mixer.blend(Profile, user=user)
    path = reverse('edit')
    request = factory.get(path)
    request.user = user
    response = edit(request)
    assert response.status_code == 200

    request = factory.post(path, {'username': 'admin', 'first_name': 'roman', 'last_name': 'grek',
                                  'email': 'roman.grek@gmail.com', 'password': 'lahsdflk344',
                                  'password2': 'lahsdflk344'}, follow=True)
    request.user = user
    response = edit(request)
    assert response.status_code == 200


def test_activate_view(client, django_user_model):
    user = django_user_model.objects.create_user(username='roman', password='password', email='roman.grek@gmail.com')
    Profile.objects.create(user=user)
    path = reverse('activate', kwargs={'uidb64': 1, 'token': 1})
    response = client.post(path, follow=True)
    assert response.status_code == 200

    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    client.force_login(user)
    response = client.post(path, follow=True)
    assert response.status_code == 200


def test_send(client, django_user_model):
    superuser = django_user_model.objects.create_superuser(username='roman',
                                                           password='password', email='roman.grek@gmail.com')
    user = django_user_model.objects.create_user(username='user1', password='123456', email='roman.grek@gmail.com')
    Profile.objects.create(user=user)
    client.force_login(superuser)
    path = reverse('admin_email_message', kwargs={'user_id': Profile.objects.get(user=user).id})
    response = client.get(path, follow=True)
    assert response.status_code == 200
