from django.contrib import admin
from django.urls import path

from playlists.views import MovieListView, TvShowListView, \
    FeaturedPlaylistListView, MovieDetailView, PlaylistDetailView, \
    TvShowDetailView,TvShowSeasonDetailView


urlpatterns = [
    path("", FeaturedPlaylistListView.as_view()),
    path("admin/", admin.site.urls),
    path("movies/", MovieListView.as_view()),
    path("movies/<slug:slug>/", MovieDetailView.as_view()),
    path("media/<int:pk>/", PlaylistDetailView.as_view()),
    path("shows/<slug:showSlug>/seasons/<slug:seasonSlug>/", TvShowSeasonDetailView.as_view()),
    path("shows/<slug:slug>/seasons/", TvShowDetailView.as_view()),
    path("shows/<slug:slug>/", TvShowDetailView.as_view()),
    path("shows/", TvShowListView.as_view()),
]
