from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.TaskListView.as_view(), name='list'),
    path('complete/<int:uid>', views.complete_task, name='complete'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('delete/<int:uid>', views.delete_task, name='delete'),
]
