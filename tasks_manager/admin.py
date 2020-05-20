from django.contrib import admin
from .models import TodoItem, TodoTable, Comment, Category


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(TodoTable)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('table', 'text', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
