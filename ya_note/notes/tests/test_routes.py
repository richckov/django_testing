from http import HTTPStatus

from .conftest import URL, MainTestCase, AUTHOR, USER, ANON


class TestRoutes(MainTestCase):
    def test_pages_for_anonymous_user(self):
        urls = (
            (URL.homepage, self.client, HTTPStatus.OK, ANON),
            (URL.login, self.client, HTTPStatus.OK, ANON),
            (URL.logout, self.client, HTTPStatus.OK, ANON),
            (URL.signup, self.client, HTTPStatus.OK, ANON),
            (URL.detail, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.edit, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.delete, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.add, self.user_client, HTTPStatus.OK, USER),
            (URL.list, self.user_client, HTTPStatus.OK, USER),
            (URL.success, self.user_client, HTTPStatus.OK, USER),
            (URL.detail, self.user_client, HTTPStatus.NOT_FOUND, USER),
            (URL.edit, self.user_client, HTTPStatus.NOT_FOUND, USER),
            (URL.delete, self.user_client, HTTPStatus.NOT_FOUND, USER),
        )
        for url, client, expected_status, user in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                )

    def test_redirect(self):
        urls = (
            URL.list,
            URL.add,
            URL.success,
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{URL.login}?next={url}'
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url,
                )
