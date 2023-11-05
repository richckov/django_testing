from collections import namedtuple
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
import pytest

from news.models import Comment, News

AUTHOR: str = lazy_fixture('author_login')
ADMIN: str = lazy_fixture('admin_client')
ANON = lazy_fixture('client')
ID: int = 1
QUANTITY_TEST: int = 5


URL_NAMES: any = namedtuple(
    'APP_NAME',
    [
        'homepage',
        'detail',
        'edit',
        'delete',
        'login',
        'logout',
        'signup'
    ],
)

URL: tuple = URL_NAMES(
    reverse('news:home'),
    reverse('news:detail', args=(ID,)),
    reverse('news:edit', args=(ID,)),
    reverse('news:delete', args=(ID,)),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


@pytest.fixture
def author(django_user_model):
    """Автор."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_login(author, client):
    """Залогиненный автор."""
    client.force_login(author)
    return client


@pytest.fixture
def news():
    """Новость."""
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def all_news():
    """Все новости."""
    all_news = News.objects.bulk_create(
        News(
            title=f'Заголовок {i}',
            text=f'Текст {i}',
            date=datetime.today().date() - timedelta(days=i)
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return all_news


@pytest.fixture
def comment(news, author):
    """Комменатрий."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def all_comments(news, author):
    """Все комментарии."""
    for i in range(QUANTITY_TEST):
        craete_comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Комменатрий {i}'
        )
        craete_comment.created = timezone.now() + timedelta(days=i)
        craete_comment.save()
    return craete_comment


@pytest.fixture
def form_text():
    """Текст формы"""
    return {
        'text': 'Новый текст комментария',
    }
