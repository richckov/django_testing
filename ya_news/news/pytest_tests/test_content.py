import pytest
from django.conf import settings

from .conftest import URL
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_order_and_count(client, all_news):
    response = client.get(URL.homepage)
    object_list = list(response.context['object_list'])
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comment_order(client, news, all_comments):
    response = client.get(URL.detail)
    assert 'news' in response.context
    news = response.context['news']
    comments_all = list(news.comment_set.all())
    assert comments_all == sorted(comments_all, key=lambda x: x.created)


def test_form_anon(client, admin_client, news):
    response = client.get(URL.detail)
    admin_response = admin_client.get(URL.detail)
    assert (
        isinstance(admin_response.context['form'], CommentForm)
        and 'form' not in response.context
    )
