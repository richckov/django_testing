from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .conftest import URL, ADMIN, AUTHOR, ANON


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, param_client, expected_status',
    (
        (URL.homepage, ANON, HTTPStatus.OK),
        (URL.detail, ANON, HTTPStatus.OK),
        (URL.login, ANON, HTTPStatus.OK),
        (URL.logout, ANON, HTTPStatus.OK),
        (URL.signup, ANON, HTTPStatus.OK),
        (URL.edit, AUTHOR, HTTPStatus.OK),
        (URL.delete, AUTHOR, HTTPStatus.OK),
        (URL.edit, ADMIN, HTTPStatus.NOT_FOUND),
        (URL.delete, ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability(
        url, param_client, expected_status, comment
):
    response = param_client.get(url)
    assert expected_status == response.status_code


@pytest.mark.parametrize(
    'url',
    (URL.edit, URL.delete),
)
def test_redirect_for_anonymous(client, url):
    expected_url = f'{URL.login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
