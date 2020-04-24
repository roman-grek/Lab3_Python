from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.tasks_list, name='list'),
    path('complete/<int:uid>', views.complete_task, name='complete'),
    path('add-task/', views.add_task, name='add-task'),
    path('create/', views.create_task, name='create'),
    path('delete/<int:uid>', views.delete_task, name='delete'),
]
