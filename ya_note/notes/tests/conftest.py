from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER_M = get_user_model()


SLUG: str = 'note-slug'
FIELD_NAMES: tuple = ('title', 'text', 'slug', 'author')
FIELD_DATA: tuple = ('Заголовок', 'Заметочка', SLUG)
FIELD_NEW_DATA: tuple = ('Новый заголовок', 'Новая заметка', 'new-slug')

AUTHOR: str = 'Автор'
USER: str = 'Юзер'
ANON: str = 'Аноним'

URL_NAME = namedtuple(
    'APP_NAME',
    [
        'homepage',
        'add',
        'list',
        'detail',
        'edit',
        'delete',
        'success',
        'login',
        'logout',
        'signup',
    ],
)

URL: tuple = URL_NAME(
    reverse('notes:home'),
    reverse('notes:add'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
    reverse('notes:success'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


class MainTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = USER_M.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = USER_M.objects.create(username=USER)
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            **dict(zip(FIELD_NAMES, (*FIELD_DATA, cls.author)))
        )
