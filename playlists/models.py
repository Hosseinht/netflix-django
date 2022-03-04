from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from netflixproject.db.models import PublishStateOptions
from netflixproject.db.receivers import publish_state_pre_save, slugify_pre_save

from categories.models import Category
from tags.models import TaggedItem
from videos.models import Video


class PlaylistQuerySet(models.QuerySet):
    # customize queryset filtering
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
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
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = "TVS", "TV Show"
        SEASON = "SEA", "Season"
        PLAYLIST = "PLA", "Playlist"

    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="playlists",
    )
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=220)
    type = models.CharField(
        max_length=3,
        choices=PlaylistTypeChoices.choices,
        default=PlaylistTypeChoices.PLAYLIST,
    )
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(
        Video,
        null=True,
        blank=True,
        related_name="playlist_featured",
        on_delete=models.SET_NULL,
    )
    # so Video can hav multiple playlist
    videos = models.ManyToManyField(
        Video,
        related_name="playlist_item",
        blank=True,
        through="PlaylistItem",
    )
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=2,
        choices=PublishStateOptions.choices,
        default=PublishStateOptions.DRAFT,
    )
    publish_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    tags = GenericRelation(TaggedItem, related_query_name="playlist")

    # we want to set timestamp when state toggle one
    # approach is override save method. we can use signals also

    objects = PlaylistManager()

    def __str__(self):
        return str(self.title)

    @property
    def is_published(self):
        return self.active


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-timestamp"]

    # manytomany field for Playlist


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)
        # get_queryset() is a method in PlaylistManager
        # which return queryset from PlaylistQuerySet


class MovieProxy(Playlist):
    """
    This will show all parents playlists
    """

    objects = MovieProxyManager()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args, **kwargs)
        # without save, it will show up in the playlist admin


class TvShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(
            parent__isnull=True, type=Playlist.PlaylistTypeChoices.SHOW
        )
        # get_queryset() is a method in PlaylistManager
        # which return queryset from PlaylistQuerySet


class TvShowProxy(Playlist):
    """
    This will show all parents playlists
    """

    objects = TvShowProxyManager()

    class Meta:
        verbose_name = "Tv Show"
        verbose_name_plural = "Tv Shows"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args, **kwargs)


class TvShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(
            parent__isnull=False, type=Playlist.PlaylistTypeChoices.SEASON
        )
        # get_queryset() is a method in PlaylistManager
        # which return queryset from PlaylistQuerySet


class TvShowSeasonProxy(Playlist):
    """
    This will show all the seasons of a tv series
    seasons of that parent playlist
    for example parent playlist is The Office
    and seasons playlists will be The Office Season 1
    The Office Season 2 etc.
    """

    objects = TvShowSeasonProxyManager()

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args, **kwargs)


pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)
