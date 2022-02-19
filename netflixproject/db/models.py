from django.db import models


class PublishStateOptions(models.TextChoices):
    # Constant = db_value, user_display_value
    PUBLISH = "PU", "Publish"
    DRAFT = 'DR', 'Draft'
