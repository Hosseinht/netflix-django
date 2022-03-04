from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from netflixproject.db.models import PublishStateOptions
from playlists.models import Playlist
from videos.models import Video


class PlaylistModelTestCase(TestCase):
    def creat_parent_playlist_with_children(self):
        the_office = Playlist.objects.create(title="The Office Series")
        # parent playlist

        # children playlist
        season_1 = Playlist.objects.create(
            title="The Office Series Season 1", parent=the_office, order=1
        )
        season_2 = Playlist.objects.create(
            title="The Office Series Season 2", parent=the_office, order=2
        )
        season_3 = Playlist.objects.create(
            title="The Office Series Season 3", parent=the_office, order=3
        )
        self.parent_playlist = the_office

    def create_videos(self):
        video_a = Video.objects.create(title="Vide title", video_id="abc")
        video_b = Video.objects.create(title="Vide title", video_id="abcd")
        video_c = Video.objects.create(title="Vide title", video_id="abce")
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c

        self.video_qs = Video.objects.all()

    def setUp(self) -> None:
        """
        This method add data to the database
        """
        self.creat_parent_playlist_with_children()
        self.create_videos()
        self.playlist_obj_a = Playlist.objects.create(
            title="This is my title", video=self.video_a
        )
        playlist_obj_b = Playlist.objects.create(
            title="This is my title",
            state=PublishStateOptions.PUBLISH,
            video=self.video_a,
        )
        # playlist_obj_b.videos.set(
        #     [self.video_a, self.video_b, self.video_c]
        # )
        # set is because of ManyToMany field
        playlist_obj_b.videos.set(self.video_qs)
        playlist_obj_b.save()
        self.playlist_obj_b = playlist_obj_b

    def test_a_show_has_seasons(self):
        seasons = self.parent_playlist.playlist_set.all()
        self.assertTrue(seasons.exists())
        self.assertEqual(seasons.count(), 3)

    def test_playlist_video(self):
        self.assertEqual(self.playlist_obj_a.video, self.video_a)

    def test_playlist_video_items(self):
        # we expect 3 videos
        count = self.playlist_obj_b.videos.all().count()
        self.assertEqual(count, 3)

    def test_playlist_through_model(self):
        video_qs = sorted(list(self.video_qs.values_list("id")))
        # query all video in Video model
        playlist_obj_video_qs = sorted(
            list(self.playlist_obj_b.videos.all().values_list("id"))
        )
        # query all the videos that is in playlist_obj_b
        playlist_obj_playlist_item_qs = sorted(
            list(self.playlist_obj_b.playlistitem_set.all().values_list("video"))
        )
        # query PlaylistItem in Playlist model

        # all these should have the same video ids in them
        self.assertEqual(video_qs, playlist_obj_video_qs, playlist_obj_playlist_item_qs)

    def test_video_playlist_ids_property(self):
        # get_playlist_ids is a method in Video model
        # which return all playlist ids that the video is in it
        ids = self.playlist_obj_a.video.get_playlist_ids()
        # obj_a has a foreign key relation with video_a
        # , so we have the playlist id in the Video object

        actual_ids = list(
            Playlist.objects.filter(video=self.video_a).values_list("id", flat=True)
        )
        # id of the playlist that filtered by the video_a
        self.assertEqual(ids, actual_ids)

    def test_video_playlist(self):
        qs = self.video_a.playlist_featured.all()

        self.assertEqual(qs.count(), 2)

    def test_valid_title(self):
        title = "This is my title"
        qs = Playlist.objects.filter(title=title)

        self.assertTrue(qs.exists())

    def test_slug_field(self):
        title = self.playlist_obj_a.title
        test_slug = slugify(title)

        self.assertEqual(test_slug, self.playlist_obj_a.slug)
        # slug create automatically base on title
        # so here we get a query set slugify its title here
        # then compare it with th e slug that automatically created

    def test_created_count(self):
        qs = Playlist.objects.all()

        self.assertEqual(qs.count(), 6)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)

        self.assertEqual(qs.count(), 5)

    def test_publish_case(self):
        # qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
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
