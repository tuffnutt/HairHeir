from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
import pytest
from booking.models import User, City
from booking.views import user, Search, AdvancedSearch


@pytest.mark.django_db
class TestViews:

    def test_user_authenticated(self):
        mixer.blend('booking.User')
        path = reverse('user', kwargs={'user_id': 2})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = user(request, user_id=2)
        assert response.status_code == 200

    def test_user_unauthenticated(self):
        mixer.blend('booking.User')
        path = reverse('user', kwargs={'user_id': 2})
        request = RequestFactory().post(path)
        request.user = AnonymousUser()

        response = user(request, user_id=2)
        assert 'accounts/login' in response.url

    def test_search(self):

        path = reverse('search')
        request = RequestFactory().post(path)

        response = Search(request)
        assert response.status_code == 200


