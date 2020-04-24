from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import TodoItem
from .forms import AddTaskForm, TodoItemForm


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


def add_task(request):
    if request.method == 'POST':
        desc = request.POST['description']
        item = TodoItem(description=desc)
        item.save()
    return redirect("/tasks/list")


def create_task(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/tasks/list")
    else:
        form = TodoItemForm()

    return render(request, "tasks/create.html", {'form': form})


def delete_task(request, uid):
    item = TodoItem.objects.get(id=uid)
    item.delete()
    return redirect('/tasks/list')
