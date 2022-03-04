from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.test import TestCase

from tags.models import TaggedItem
from playlists.models import Playlist


class TaggedItemTestCase(TestCase):
    def setUp(self) -> None:
        playlist_title = "My Title"
        self.playlist_a = Playlist.objects.create(title=playlist_title)
        self.playlist_title = playlist_title
        self.playlist_a.tags.add(
            TaggedItem(tag='new-tag'),
            bulk=False
        )

    def test_content_type_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            self.tag_a = TaggedItem.objects.create(tag='new-tag')
            # content_type

    def test_create_via_content_type(self):
        content_type = ContentType.objects.get(
            app_label='playlists',
            model='playlist'
        )
        tag_a = TaggedItem.objects.create(
            tag='new-tag',
            content_type=content_type,
            object_id=1
        )
        tag_b = TaggedItem.objects.create(
            tag='new-tag2',
            content_type=content_type,
            object_id=10
        )
        self.assertIsNotNone(tag_a.pk)
        self.assertIsNotNone(tag_b.pk)

    def test_create_via_model_content_type(self):
        content_type = ContentType.objects.get_for_model(Playlist)
        tag_a = TaggedItem.objects.create(
            tag='new-tag',
            content_type=content_type,
            object_id=1
        )
        self.assertIsNotNone(tag_a.pk)

    def test_create_via_app_loader_content_type(self):
        playlistclass = apps.get_model(
            app_label='playlists',
            model_name='playlist'
        )
        content_type = ContentType.objects.get_for_model(playlistclass)
        tag_a = TaggedItem.objects.create(
            tag='new-tag',
            content_type=content_type,
            object_id=1
        )
        self.assertIsNotNone(tag_a.pk)

    def test_related_field(self):
        self.assertEqual(self.playlist_a.tags.count(), 1)

    def test_related_field_create(self):
        self.playlist_a.tags.create(tag='another-tag')
        self.assertEqual(self.playlist_a.tags.count(), 2)

    def test_related_field_query_name(self):
        qs = TaggedItem.objects.filter(playlist__title__iexact=self.playlist_title)
        self.assertEqual(qs.count(), 1)

    def test_related_field_via_content_type(self):
        content_type = ContentType.objects.get_for_model(Playlist)
        tag_qs = TaggedItem.objects.filter(
            content_type=content_type,
            object_id=self.playlist_a.id
        )
        self.assertEqual(tag_qs.count(), 1)
