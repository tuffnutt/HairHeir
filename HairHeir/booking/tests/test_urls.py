from django.urls import resolve, reverse
import pytest

@pytest.mark.django_db
class TestUrls:
    def test_user(self):
        path = reverse('user', kwargs={'user_id': 2})
        assert resolve(path).view_name == 'user'

    def test_search(self):
        path = reverse('search')
        assert resolve(path).view_name == 'search'

    def test_home(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def test_advancedsearch(self):
        path = reverse('advancedsearch')
        assert resolve(path).view_name == 'advancedsearch'

    def test_signup(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'

    def test_client_signup(self):
        path = reverse('client_signup')
        assert resolve(path).view_name == 'client_signup'

    def test_freelancer_signup(self):
        path = reverse('freelancer_signup')
        assert resolve(path).view_name == 'freelancer_signup'
