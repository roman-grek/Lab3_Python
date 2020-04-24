from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import TodoItem


def index(request):
    return HttpResponse("Примитивный ответ из приложения tasks_manager")


def tasks_list(request):
    all_tasks = TodoItem.objects.all()
    return render(
        request,
        'tasks_manager/list.html',
        {'tasks': all_tasks}
    )


def complete_task(request, uid):

    return HttpResponse('OK')


def delete_task(request, uid):

    return redirect('/tasks_manager/list')
