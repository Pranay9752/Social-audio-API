from django.conf.urls import url

from .views import TrendingGenreView, MasterSearchView, UserSearchView, AlbumSearchView, SongSearchView, PodcastSearchView

app_name='searh'
urlpatterns = [
    url(r'^trending/$', TrendingGenreView.as_view(),name='trend_genre'),
    url(r'^user/$', UserSearchView.as_view(),name='user_search'),
    url(r'^album/$', AlbumSearchView.as_view(),name='album_search'),
    url(r'^song/$', SongSearchView.as_view(),name='song_search'),
    url(r'^podcast/$', PodcastSearchView.as_view(),name='podcast_search'),
    url(r'^', MasterSearchView.as_view(),name='master_search'),
    
]
