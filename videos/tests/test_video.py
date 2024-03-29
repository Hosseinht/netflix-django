from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from netflixproject.db.models import PublishStateOptions
from videos.models import Video


class VideoModelTestCase(TestCase):
    def setUp(self) -> None:
        """
        This method add data to the database
        """
        self.obj_a = Video.objects.create(title="This is my title", video_id="123")
        self.obj_b = Video.objects.create(
            title="This is my title",
            state=PublishStateOptions.PUBLISH,
            video_id="1234",
        )

    def test_valid_title(self):
        title = "This is my title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)
        # self.assertEqual(test_slug, 'this-is-my-title')
        # slug create automatically base on title
        # so here we get a query set slugify its title here
        # then compare it with th e slug that automatically created

    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        # qs = Video.objects.filter(state=PublishStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )
        # we have published_timestamp when
        # state = PublishStateOptions.PUBLISH
        # so if state = PublishStateOptions.PUBLISH test will fail
        self.assertTrue(published_qs.exists())

    def test_published_manager(self):
        published_qs = Video.objects.all().published()
        published_qs2 = Video.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs2.count())
