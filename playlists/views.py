from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Playlist, MovieProxy, TvShowProxy, TvShowSeasonProxy


class PlaylistMixin():
    template_name = 'playlist_list.html'
    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.title is not None:
            context['title'] = self.title
        print(context)
        return context

    def get_queryset(self):
        return super().get_queryset().published()


class MovieListView(PlaylistMixin, ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"


class MovieDetailView(PlaylistMixin, DetailView):
    queryset = MovieProxy.objects.all()
    template_name = 'playlists/movie_detail.html'
    title = "Movies"
    # context_object_name = "instance"


class PlaylistDetailView(PlaylistMixin, DetailView):
    queryset = Playlist.objects.all()
    template_name = 'playlists/playlist_detail.html'


class TvShowListView(PlaylistMixin, ListView):
    queryset = TvShowProxy.objects.all()
    title = "Tv Shows"


class TvShowDetailView(PlaylistMixin, DetailView):
    queryset = TvShowProxy.objects.all()
    template_name = 'playlists/tvshow_detail.html'


class TvShowSeasonDetailView(PlaylistMixin, DetailView):
    queryset = TvShowSeasonProxy.objects.all()
    template_name = 'playlists/season_detail.html'

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get('showSlug')
        season_slug = kwargs.get('seasonSlug')
        qs = self.get_queryset().filter(
            parent__slug__iexact=show_slug,
            slug__iexact=season_slug
        )
        if not qs.count() == 1:
            raise Http404
        return qs.first()


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    queryset = Playlist.objects.featured_playlist()
    title = "Featured"
