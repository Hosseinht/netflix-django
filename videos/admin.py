from django.contrib import admin
from .models import VideoPublishedProxy, VideoAllProxy


class VideoAllAdmin(admin.ModelAdmin):
    """
        All videos
    """
    list_display = ["title", "video_id"]
    search_fields = ['title']

    class Meta:
        model = VideoAllProxy


class VideoProxyAdmin(admin.ModelAdmin):
    list_display = ["title", "video_id"]
    search_fields = ['title']

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)
    # so here we will have only published videos and all videos in the video admin


admin.site.register(VideoAllProxy, VideoAllAdmin)
admin.site.register(VideoPublishedProxy, VideoProxyAdmin)
