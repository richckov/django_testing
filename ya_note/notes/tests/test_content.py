from notes.forms import NoteForm
from .conftest import URL, MainTestCase


class TestNoteList(MainTestCase):
    def test_notes_list_for_others_users(self):
        clients = (
            (self.author_client, True),
            (self.user_client, False),
        )
        for client, value in clients:
            with self.subTest(client=client):
                object_list = client.get(URL.list).context['object_list']
                self.assertTrue(
                    (self.note in object_list) is value,
                )

    def test_pages_form(self):
        for url in (URL.add, URL.edit):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context['form'],
                    NoteForm,
                )
