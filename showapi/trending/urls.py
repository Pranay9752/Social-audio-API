from django.conf.urls import url
from .views import TrendingStoriesView, TrendingSongView, TrendingAlbumView, TrendingPodcastView, TrendingPlaylistView
urlpatterns = [

    url(r'^stories/$',TrendingStoriesView.as_view(),name='trending_stories'),
    url(r'^songs/$',TrendingSongView.as_view(),name='trending_songs'),
    url(r'^albums/$',TrendingAlbumView.as_view(),name='trending_albums'),
    url(r'^podcasts/$',TrendingPodcastView.as_view(),name='trending_podcasts'),
    url(r'^playlists/$',TrendingPlaylistView.as_view(),name='trending_playlists'),
]