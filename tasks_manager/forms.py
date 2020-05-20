from django import forms

from .models import TodoItem, TodoTable, Comment


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description', 'table')
        labels = {'description': '', 'table': ''}


class TodoTableForm(forms.ModelForm):
    class Meta:
        model = TodoTable
        fields = ('title', 'category',)
        labels = {'title': ''}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
