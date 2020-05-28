from django.urls import reverse, resolve


class TestUrls:

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_register_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_edit_url(self):
        path = reverse('edit')
        assert resolve(path).view_name == 'edit'

    def test_password_change_url(self):
        path = reverse('password_change')
        assert resolve(path).view_name == 'password_change'

    def test_password_change_done_url(self):
        path = reverse('password_change_done')
        assert resolve(path).view_name == 'password_change_done'
