from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from netflixproject.db.models import PublishStateOptions
from playlists.models import Playlist, MovieProxy
from videos.models import Video


class MovieProxyTestCase(TestCase):

    def create_videos(self):
        video_a = Video.objects.create(title="Vide title", video_id="abc")
        video_b = Video.objects.create(title="Vide title", video_id="abcd")
        video_c = Video.objects.create(title="Vide title", video_id="abce")
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c

        self.video_qs = Video.objects.all()

    def setUp(self) -> None:
        self.create_videos()
        self.movie_title = "This is my title"
        self.published_item_count = 1
        self.movie_a = MovieProxy.objects.create(
            title=self.movie_title, video=self.video_a
        )
        movie_b = MovieProxy.objects.create(
            title="This is my title",
            state=PublishStateOptions.PUBLISH,
            video=self.video_a,
        )
        # playlist_obj_b.videos.set(
        #     [self.video_a, self.video_b, self.video_c]
        # )
        # set is because of ManyToMany field
        movie_b.videos.set(self.video_qs)
        movie_b.save()
        self.movie_b = movie_b

    def test_movie_video_foreign_key(self):
        self.assertEqual(self.movie_a.video, self.video_a)

    def test_movie_clip_items(self):
        # we expect 3 videos
        count = self.movie_b.videos.all().count()
        self.assertEqual(count, 3)

    def test_valid_title(self):
        title = self.movie_title
        qs = MovieProxy.objects.filter(title=title)

        self.assertTrue(qs.exists())

    def test_slug_field(self):
        title = self.movie_title
        test_slug = slugify(title)

        self.assertEqual(test_slug, self.movie_a.slug)
        # slug create automatically base on title
        # so here we get a query set slugify its title here
        # then compare it with th e slug that automatically created

    def test_draft_case(self):
        qs = MovieProxy.objects.filter(state=PublishStateOptions.DRAFT)

        self.assertEqual(qs.count(), 1)

    def test_published_manager(self):
        published_qs = MovieProxy.objects.all().published()
        published_qs2 = MovieProxy.objects.published()

        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs2.count())
        self.assertEqual(published_qs.count(), self.published_item_count)
