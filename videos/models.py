from django.db import models
from django.utils import timezone


class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # Constant = db_value, user_display_value
        PUBLISH = "PU", "Publish"
        DRAFT = 'DR', 'Draft'

    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220)
    active = models.BooleanField(default=True)
    # timestamp
    # updated
    state = models.CharField(
        max_length=2,
        choices=VideoStateOptions.choices,
        default=VideoStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )

    # we want to set timestamp when state toggle one approach is override save method. we can use signals also

    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None

        super().save(*args, **kwargs)


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
