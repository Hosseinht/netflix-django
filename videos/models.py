from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from netflixproject.db.models import PublishStateOptions
from netflixproject.db.receivers import (
    publish_state_pre_save,
    slugify_pre_save
)


class VideoQuerySet(models.QuerySet):
    # customize queryset filtering
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
        # we want our own custom method for filtering


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    # self._db = default database

    def published(self):
        return self.get_queryset().published()
    # now we can have Vide.objects
    # .filter(title__icontains="something").publish()


# because we want to use it over and over again
# , and we want our custom method to filter

class Video(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=2,
        choices=PublishStateOptions.choices,
        default=PublishStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    # we want to set timestamp when state toggle one
    # approach is override save method. we can use signals also

    objects = VideoManager()

    @property
    def is_published(self):
        return self.active


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"


pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)
