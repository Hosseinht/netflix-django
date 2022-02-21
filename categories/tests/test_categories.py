from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from categories.models import Category
from playlists.models import Playlist


class CategoryTestCase(TestCase):
    def setUp(self) -> None:
        cat_a = Category.objects.create(title="Comedy")
        cat_b = Category.objects.create(title="Action", active=False)
        self.playlist_a = Playlist.objects.create(
            title='My Title',
            category=cat_a,
        )
        self.cat_a = cat_a
        self.cat_b = cat_b

    def test_category_is_active(self):
        self.assertTrue(self.cat_a.active)

    def test_category_is_not_active(self):
        self.assertFalse(self.cat_b.active)

    def test_related_playlist(self):
        qs = self.cat_a.playlists.all()
        self.assertEqual(qs.count(), 1)
