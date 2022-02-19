from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from netflixproject.db.models import PublishStateOptions
from netflixproject.db.receivers import (
    publish_state_pre_save,
    slugify_pre_save
)

from videos.models import Video


class PlaylistQuerySet(models.QuerySet):
    # customize queryset filtering
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
        # we want our own custom method for filtering


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    # self._db = default database

    def published(self):
        return self.get_queryset().published()
    # now we can have Vide.objects
    # .filter(title__icontains="something").publish()


# because we want to use it over and over again
# , and we want our custom method to filter

class Playlist(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(
        Video,
        null=True,
        related_name='playlist_featured',
        on_delete=models.SET_NULL
    )
    # so Video can hav multiple playlist
    videos = models.ManyToManyField(
        Video,
        related_name='playlist_item',
        blank=True
    )
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

    objects = PlaylistManager()

    @property
    def is_published(self):
        return self.active


pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)
