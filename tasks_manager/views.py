from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TodoItem
from .forms import AddTaskForm, TodoItemForm


@login_required
def index(request):
    return HttpResponse("Примитивный ответ из приложения tasks")


class TaskListView(LoginRequiredMixin, ListView):
    model = TodoItem
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()


class TaskCreateView(View):
    def create_render(self, request, form):
        return render(request, "tasks/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('tasks:list')

        return self.create_render(request, form)

    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return self.create_render(request, form)


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'


def complete_task(request, uid):
    item = TodoItem.objects.get(id=uid)
    item.is_completed = not item.is_completed
    item.save()
    return HttpResponse('OK')


def delete_task(request, uid):
    item = TodoItem.objects.get(id=uid)
    item.delete()
    return redirect('tasks:list')


def add_task(request):
    if request.method == "POST":
        desc = request.POST["description"]
        t = TodoItem(description=desc)
        t.save()
    return redirect("tasks:list")
