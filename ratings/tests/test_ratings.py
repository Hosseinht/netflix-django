import random
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.test import TestCase

from playlists.models import Playlist
from ratings.models import Rating, RatingChoices

User = get_user_model()


class RatingTestCase(TestCase):
    def create_playlists(self):
        items = []
        self.playlist_count = random.randint(10, 500)
        for i in range(0, self.playlist_count):
            items.append(Playlist(title=f'Tv show {i}'))
        Playlist.objects.bulk_create(items)
        self.playlists = Playlist.objects.all()

    def create_users(self):
        items = []
        self.user_count = random.randint(10, 700)
        for i in range(0, self.user_count):
            items.append(User(username=f"user_{i}"))
        User.objects.bulk_create(items)
        self.users = User.objects.all()

    def create_ratings(self):
        items = []
        self.rating_totals = []
        self.rating_count = 1_000
        for i in range(0, self.rating_count):
            user_obj = self.users.order_by("?").first()
            ply_obj = self.playlists.order_by("?").first()
            rating_val = random.choice(RatingChoices.choices)[0]
            if rating_val is not None:
                self.rating_totals.append(rating_val)
            items.append(
                Rating(
                    user=user_obj,
                    content_object=ply_obj,
                    value=rating_val
                )
            )
        Rating.objects.bulk_create(items)
        self.ratings = Rating.objects.all()

    def setUp(self) -> None:
        self.create_users()
        self.create_playlists()
        self.create_ratings()

    def test_user_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.user_count)
        self.assertEqual(self.users.count(), self.user_count)

    def test_playlist_count(self):
        qs = Playlist.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.playlist_count)
        self.assertEqual(self.playlists.count(), self.playlist_count)

    def test_rating_count(self):
        qs = Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.rating_count)
        self.assertEqual(self.ratings.count(), self.rating_count)

    def test_rating_random_choices(self):
        value_set = set(Rating.objects.values_list('value', flat=True))
        self.assertTrue(len(value_set) > 1)

    def test_rating_agg(self):
        item_1 = Rating.objects.aggregate(
            average=Avg('value')
        )['average']
        self.assertIsNotNone(item_1)
        self.assertTrue(item_1 > 0)

    def test_rating_playlist_agg(self):
        item_1 = Playlist.objects.aggregate(
            average=Avg('ratings__value')
        )['average']
        self.assertIsNotNone(item_1)
        self.assertTrue(item_1 > 0)


