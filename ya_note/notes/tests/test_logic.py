from http import HTTPStatus

from django.test import Client, TestCase
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .conftest import (
    MainTestCase,
    FIELD_DATA,
    FIELD_NAMES,
    FIELD_NEW_DATA,
    AUTHOR,
    URL,
    SLUG,
    USER_M,
)


class TestCreateNote(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = USER_M.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.form_data = dict(zip(FIELD_NAMES, FIELD_DATA))
        cls.field_data = (*FIELD_DATA, cls.author)

    def test_user_create_note(self):
        expected_count = Note.objects.count() + 1
        self.assertRedirects(
            self.author_client.post(URL.add, data=self.form_data),
            URL.success,
        )
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
        )
        note = Note.objects.get()
        db_data = (note.title, note.text, note.slug, note.author)
        for name, sent_value, db_value in zip(
                FIELD_NAMES, self.field_data, db_data
        ):
            with self.subTest(sent_value=sent_value, db_value=db_value):
                self.assertEqual(
                    sent_value,
                    db_value,
                )

    def test_anonymous_user_create_note(self):
        expected_count = Note.objects.count()
        expected_url = f'{URL.login}?next={URL.add}'
        self.assertRedirects(
            self.client.post(URL.add, data=self.form_data),
            expected_url,
        )
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
        )

    def test_not_unique_slug(self):
        expected_count = Note.objects.count() + 1
        Note.objects.create(**dict(zip(FIELD_NAMES, self.field_data)))
        self.assertFormError(
            self.author_client.post(URL.add, data=self.form_data),
            form='form',
            field='slug',
            errors=(SLUG + WARNING),
        )
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
        )

    def test_empty_slug(self):
        expected_count = Note.objects.count() + 1
        self.form_data.pop('slug')
        self.assertRedirects(
            self.author_client.post(URL.add, data=self.form_data),
            URL.success,
        )
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
        )
        note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(
            note.slug,
            expected_slug,
        )


class TestNoteEditDelete(MainTestCase, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_data = dict(zip(FIELD_NAMES, FIELD_NEW_DATA))

    def test_author_edit_note(self):
        self.assertRedirects(
            self.author_client.post(URL.edit, data=self.new_data),
            URL.success,
        )
        note = Note.objects.get()
        db_data = (note.title, note.text, note.slug, note.author)
        field_data = (*FIELD_NEW_DATA, self.author)
        for name, sent_value, db_value in zip(
                FIELD_NAMES, field_data, db_data
        ):
            with self.subTest(sent_value=sent_value, db_value=db_value):
                self.assertEqual(
                    sent_value,
                    db_value,
                )

    def test_author_delete_note(self):
        expected_count = Note.objects.count() - 1
        self.assertRedirects(
            self.author_client.delete(URL.delete),
            URL.success,
        )
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
        )

    def test_other_user_edit_note(self):
        self.assertEqual(
            self.user_client.post(URL.edit, data=self.new_data).status_code,
            HTTPStatus.NOT_FOUND,
        )
        note = Note.objects.get()
        db_data = (note.title, note.text, note.slug, note.author)
        field_data = (*FIELD_DATA, self.author)
        for name, sent_value, db_value in zip(
                FIELD_NAMES, field_data, db_data
        ):
            with self.subTest(sent_value=sent_value, db_value=db_value):
                self.assertEqual(
                    sent_value,
                    db_value,
                )

    def test_other_user_delete_note(self):
        expected_count = Note.objects.count()
        self.assertEqual(
            self.user_client.delete(URL.delete).status_code,
            HTTPStatus.NOT_FOUND,
        )
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
        )
