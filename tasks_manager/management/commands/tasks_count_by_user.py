from django.contrib.auth.models import User
from django.core.management import BaseCommand
from collections import Counter

from tasks_manager.models import TodoItem


class Command(BaseCommand):
    help = u"Count tasks for all users and print top-`users-count`(default 25) users"

    def add_arguments(self, parser):
        parser.add_argument('--users-count', dest='users-count', type=int, default=25)

    def handle(self, *args, **options):
        users = Counter()
        for u in User.objects.all():
            for t in u.tasks.all():
                users[u] += 1

        index = 1
        for user, amount in users.most_common(options['users-count']):
            print(f"{index}.{user} {amount}")
            index += 1
