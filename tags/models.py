from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.tag

    # pass in an actual object, category with the id of 1 and
    # reference it to this tag now
    # so with content type we can choose playlist, video etc.
    # and object-id
    # is the id of that playlist or video.

    """
        Contenttype.objects.all(): 
        we will see every app and model in our project.
        now we want to grab the category so:
        id = 1
        cat_type = Contenttype.objects.get(
            app_label='categories',
            model = 'category'
        )
        so now cat_type is:
        <ContentType: categories | Category>
        now we want model class itself so:
        cat_type.model_class()
        it will return this:
        <class 'categories.models.Category'>
        so now we have category model and we can get the categories:
        Category.objects.get(id=1)
        <Category: Action>
    """
