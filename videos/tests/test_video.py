from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from videos.models import Video


class VideoModelTestCase(TestCase):
    def setUp(self) -> None:
        """
            This method add data to the database
        """
        self.obj_a = Video.objects.create(
            title="This is my title",
            video_id="123"
        )
        self.obj_b = Video.objects.create(
            title="This is my title",
            state=Video.VideoStateOptions.PUBLISH,
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
        # slug create automatically base on title
        # so here we get a query set slugify its title here
        # then compare it with th e slug that automatically created

    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        # qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=Video.VideoStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
        # we have published_timestamp when
        # state = Video.VideoStateOptions.PUBLISH
        # so if state = Video.VideoStateOptions.PUBLISH test will fail
        self.assertTrue(published_qs.exists())
