from django.contrib import admin
from .models import Playlist, PlaylistItem, TvShowProxy, TvShowSeasonProxy


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    """
      a playlist with all its videos
      For example The Office as the parent
      and season 1 as the child and all the videos related to season 1
    """
    inlines = [PlaylistItemInline]

    class Meta:
        model = Playlist


class TvShowSeasonProxyInline(admin.TabularInline):
    model = TvShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'state']

    # def get_queryset(self, request):
    #     return TvShowSeasonProxy.objects.all()


class TvShowProxyAdmin(admin.ModelAdmin):
    """
        This one shows all the parent playlists(a Tv series like The Office)
        which contains all the season of that playlist or
        in Inline part we will see all the seasons
    """
    inlines = [TvShowSeasonProxyInline]
    fields = ['title', 'description', 'state', 'video', 'slug']

    class Meta:
        model = TvShowProxy

    def get_queryset(self, request):
        return TvShowProxy.objects.all()


class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class TvShowSeasonProxyAdmin(admin.ModelAdmin):
    """
        This one shows all the seasons and the videos related to that season
    """
    inlines = [SeasonEpisodeInline]
    list_display = ['title', 'parent']

    class Meta:
        model = TvShowSeasonProxy

    def get_queryset(self, request):
        return TvShowSeasonProxy.objects.all()


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(TvShowProxy, TvShowProxyAdmin)
admin.site.register(TvShowSeasonProxy, TvShowSeasonProxyAdmin)
