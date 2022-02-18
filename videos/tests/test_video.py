from django.test import TestCase

from videos.models import Video


class VideoModelTestCase(TestCase):
    def setUp(self) -> None:
        """
            This method add data to the database
        """
        Video.objects.create(title="This is my title")

    def test_valid_title(self):
        title = "This is my title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())
