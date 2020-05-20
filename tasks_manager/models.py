from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    slug = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.slug


class TodoTable(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tables'
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    description = models.CharField(max_length=64)
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    table = models.ForeignKey(
        TodoTable,
        on_delete=models.CASCADE,
        related_name='tasks',
        default=0
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    table = models.ForeignKey(TodoTable, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField('Текст комментария', max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
