from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects
# from django.urls import reverse


from .conftest import URL
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news, form_text):
    """Анонимный пользователь не может создавать комментарий."""
    expected_count = Comment.objects.count()
    client.post(URL.detail, data=form_text)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count


def test_user_can_create_comment(author_login, author, news, form_text):
    """Авторизированный пользователь может создавать комментарий."""
    expected_count = Comment.objects.count() + 1
    response = author_login.post(URL.detail, data=form_text)
    comments_count = Comment.objects.count()
    new_comment = Comment.objects.get()
    assertRedirects(response, f'{URL.detail}#comments')
    assert expected_count == comments_count
    assert new_comment.text == form_text['text']
    assert new_comment.author == author
    assert new_comment.news == news


@pytest.mark.parametrize('word', BAD_WORDS)
def test_user_cant_use_bad_words(author_login, news, word):
    """Проверка на плохие слова."""
    expected_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {word}, еще текст'}
    response = author_login.post(URL.detail, data=bad_words_data)
    comments_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert expected_count == comments_count


def test_author_delete_comment(author_login, comment):
    expected_count = Comment.objects.count() - 1
    try:
        response = author_login.delete(URL.delete)
        comments_count = Comment.objects.count()
        assertRedirects(response, f'{URL.detail}#comments')
        assert expected_count == comments_count
    except comments_count != expected_count:
        print("Ошибка при удалении комментария")


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    """Другой пользователь не может удалятб комментарий."""
    expected_count = Comment.objects.count()
    response = admin_client.delete(URL.delete)
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count


def test_author_can_edit_comment(
    author, author_login, comment, form_text
):
    """Автор может редактировать комментарий."""
    expected_count = Comment.objects.count()
    response = author_login.post(URL.edit, data=form_text)
    assertRedirects(response, f'{URL.detail}#comments')
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert expected_count == comments_count


def test_user_cant_edit_comment_of_another_user(
    author, admin_client, comment, form_text
):
    """Другой пользовтаель не может редактировать комментарий."""
    expected_count = Comment.objects.count()
    response = admin_client.post(URL.edit, data=form_text)
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count
