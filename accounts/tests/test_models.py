import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from ..models import Profile


@pytest.fixture
def user(request, db):
    return mixer.blend(User, username=request.param)


@pytest.mark.parametrize('user', ['roman'], indirect=True)
def test_profile(user):
    profile = Profile.objects.create(user=user)
    assert profile.verified is False
    assert profile.__str__() == "Профиль пользователя roman"
