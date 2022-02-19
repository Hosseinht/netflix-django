from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from netflixproject.db.models import PublishStateOptions
from playlists.models import Playlist
from videos.models import Video


class PlaylistModelTestCase(TestCase):
    def setUp(self) -> None:
        """
            This method add data to the database
        """
        video_a = Video.objects.create(
            title='Vide title',
            video_id='abc'
        )
        self.video_a = video_a
        self.obj_a = Playlist.objects.create(
            title="This is my title",
            video=video_a
        )
        self.obj_b = Playlist.objects.create(
            title="This is my title",
            state=PublishStateOptions.PUBLISH,
            video=video_a,
        )

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video, self.video_a)

    def test_video_playlist(self):
        qs = self.video_a.playlist_set.all()

        self.assertEqual(qs.count(), 2)

    def test_valid_title(self):
        title = "This is my title"
        qs = Playlist.objects.filter(title=title)

        self.assertTrue(qs.exists())

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)

        self.assertEqual(test_slug, self.obj_a.slug)
        # slug create automatically base on title
        # so here we get a query set slugify its title here
        # then compare it with th e slug that automatically created

    def test_created_count(self):
        qs = Playlist.objects.all()

        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)

        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        # qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
        # we have published_timestamp when
        # state = PublishStateOptions.PUBLISH
        # so if state = PublishStateOptions.PUBLISH test will fail
        self.assertTrue(published_qs.exists())

    def test_published_manager(self):
        published_qs = Playlist.objects.all().published()
        published_qs2 = Playlist.objects.published()

        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs2.count())
