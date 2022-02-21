from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # pass in an actual object, category with the id of 1 and reference it to this tag now
    # so with content type we can choose playlist, video etc. and object-id
    # is the id of that playlist or video.
