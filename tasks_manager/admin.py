from django.contrib import admin
from .models import TodoItem, TodoTable


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(TodoTable)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
