from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TodoItem, TodoTable, Comment
from .forms import TodoItemForm, TodoTableForm, CommentForm


class TaskListView(LoginRequiredMixin, ListView):
    model = TodoTable
    context_object_name = 'tables'
    template_name = 'tasks/list.html'

    def get_queryset(self):
        user = self.request.user
        return user.tables.all()


def table_by_id(request, uid):
    table = TodoTable.objects.get(id=uid)
    items = TodoItem.objects.filter(table=table)
    return render(request, "tasks/table.html",
                  {"table": table, "tasks": items})


class TaskCreateView(View):
    def create_render(self, request, form):
        return render(request, "tasks/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('tasks:table', uid=new_task.table.id)

        return self.create_render(request, form)

    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return self.create_render(request, form)


class TaskCreateTableView(View):
    def create_render(self, request, form):
        return render(request, "tasks/create-table.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TodoTableForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('tasks:list')

        return self.create_render(request, form)

    def get(self, request, *args, **kwargs):
        form = TodoTableForm()
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
    table_id = item.table.id
    item.delete()
    return redirect('tasks:table', uid=table_id)


def delete_table(request, uid):
    item = TodoTable.objects.get(id=uid)
    item.delete()
    return redirect('tasks:list')


def delete_comment(request, uid):
    item = Comment.objects.get(id=uid)
    table_id = item.table.id
    item.delete()
    return redirect('tasks:table', uid=table_id)


def add_comment(request, uid):
    table = TodoTable.objects.get(id=uid)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.table = table
            comment.save()
            return redirect('tasks:table', uid=table.id)
    else:
        form = CommentForm()
    return render(request, 'tasks/add-comment.html', {'form': form})
