from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import TodoItem


def index(request):
    return HttpResponse("Примитивный ответ из приложения tasks")


def tasks_list(request):
    all_tasks = TodoItem.objects.all()
    return render(
        request,
        'tasks/list.html',
        {'tasks': all_tasks}
    )


def complete_task(request, uid):
    item = TodoItem.objects.get(id=uid)
    item.is_completed = not item.is_completed
    item.save()
    return HttpResponse('OK')


def delete_task(request, uid):
    item = TodoItem.objects.get(id=uid)
    item.delete()
    return redirect('/tasks/list')
