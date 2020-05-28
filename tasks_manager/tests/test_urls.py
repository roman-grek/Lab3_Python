from django.urls import reverse, resolve


class TestUrls:

    def test_list_url(self):
        path = reverse('tasks:list')
        assert resolve(path).view_name == 'tasks:list'

    def test_complete_url(self):
        path = reverse('tasks:complete', kwargs={'uid': 1})
        assert resolve(path).view_name == 'tasks:complete'

    def test_create_url(self):
        path = reverse('tasks:create')
        assert resolve(path).view_name == 'tasks:create'

    def test_create_table_url(self):
        path = reverse('tasks:create-table')
        assert resolve(path).view_name == 'tasks:create-table'

    def test_table_url(self):
        path = reverse('tasks:table', kwargs={'uid': 1})
        assert resolve(path).view_name == 'tasks:table'

    def test_delete_url(self):
        path = reverse('tasks:delete', kwargs={'uid': 1})
        assert resolve(path).view_name == 'tasks:delete'

    def test_delete_table_url(self):
        path = reverse('tasks:delete-table', kwargs={'uid': 1})
        assert resolve(path).view_name == 'tasks:delete-table'

    def test_details_url(self):
        path = reverse('tasks:details', kwargs={'pk': 1})
        assert resolve(path).view_name == 'tasks:details'

    def test_comment_url(self):
        path = reverse('tasks:add_comment', kwargs={'uid': 1})
        print(resolve(path).view_name)
        assert resolve(path).view_name == 'tasks:add_comment'

    def test_delete_comment_url(self):
        path = reverse('tasks:delete_comment', kwargs={'uid': 1})
        assert resolve(path).view_name == 'tasks:delete_comment'
