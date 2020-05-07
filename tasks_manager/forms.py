from django import forms

from .models import TodoItem, TodoTable


class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=64, label='')


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description', 'table')
        labels = {'description': '', 'table': ''}


class TodoTableForm(forms.ModelForm):
    class Meta:
        model = TodoTable
        fields = ('title',)
        labels = {'title': ''}
