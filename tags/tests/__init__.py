from django.test import TestCase

from ..models import TaggedItem


class TaggedItemTestCase(TestCase):
    def setUp(self) -> None:
        TaggedItem.objects.create()
