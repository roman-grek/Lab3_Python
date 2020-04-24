from django.db import models


class TodoItem(models.Model):
    description = models.CharField(max_length=64)
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description.lower()

    class Meta:
        ordering = ('-created',)


def parse_db_url(db_link: str) -> dict:
    result = {}
    if db_link.startswith('postgres://'):
        result['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
        db_link = db_link[11:]
        index = db_link.index(':')
        result['USER'] = db_link[:index]
        db_link = db_link[index + 1:]
        index = db_link.index('@')
        result['PASSWORD'] = db_link[:index]
        db_link = db_link[index + 1:]
        index = db_link.index(':')
        result['HOST'] = db_link[:index]
        db_link = db_link[index + 1:]
        index = db_link.index('/')
        result['PORT'] = db_link[:index]
        db_link = db_link[index + 1:]
        result['NAME'] = db_link

    elif db_link.startswith('sqlite:///'):
        result['ENGINE'] = 'django.db.backends.sqlite3'
        result['NAME'] = db_link[10:]
    else:
        raise ValueError

    for value in result.values():
        if len(value) == 0:
            raise ValueError

    return result
