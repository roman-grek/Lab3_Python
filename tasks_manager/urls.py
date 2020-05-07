from django.urls import path

from . import views


app_name = 'tasks'

urlpatterns = [
    path('list/', views.TaskListView.as_view(), name='list'),
    path('complete/<int:uid>', views.complete_task, name='complete'),
    path("add-task/", views.add_task, name="api-add-task"),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('create-table/', views.TaskCreateTableView.as_view(), name='create-table'),
    path('table/<int:uid>', views.table_by_id, name='table'),
    path('delete/<int:uid>', views.delete_task, name='delete'),
    path('delete-table/<int:uid>', views.delete_table, name='delete-table'),
    path('details/<int:pk>', views.TaskDetailsView.as_view(), name='details')
]
