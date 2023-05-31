from django.urls import path,include
from django.conf.urls import url
from rest_framework import routers

from .views import (SongCreateView,
                    AllSongListView,
                    SongListView,
                    SongDetailView,
                    AlbumCreateView,
                    AllAlbumListView,
                    AlbumListView,
                    AlbumDetailView,
                    AlbumSongView,
                    AllPodcastListView,
                    PodcastListView,
                    PodcastDetailView,
                    AllPlaylistListView,
                    PlaylistListView,
                    PlaylistDetailView,
                    )


app_name='music'
urlpatterns = [
    url(r'^song/$', SongCreateView.as_view(),name='song_create'),
    url(r'^songs/$', SongListView.as_view(),name='my_songs_list'),
    url(r'^songs/all/$', AllSongListView.as_view(),name='songs_list'),
    url(r'^s/(?P<pk>.+)/$', SongDetailView.as_view(),name='song'),

    url(r'^album/$', AlbumCreateView.as_view(),name='album_create'),
    url(r'^albums/all/$', AllAlbumListView.as_view(),name='all_album_list'),
    url(r'^albums/$', AlbumListView.as_view(),name='album_list'),
    url(r'^album/(?P<pk>.+)/$', AlbumDetailView.as_view(),name='album_detail'),
    url(r'^songentry/$', AlbumSongView.as_view(),name='albm_song'),

    url(r'^podcast/all/$', AllPodcastListView.as_view(),name='all_podcast_list'),
    url(r'^podcasts/$', PodcastListView.as_view(),name='podcast_list'),
    url(r'^podcast/(?P<pk>.+)/$', PodcastDetailView.as_view(),name='podcast_detail'),

    url(r'^playlists/all/$', AllPlaylistListView.as_view(),name='all_playlist_list'),
    url(r'^playlists/$', PlaylistListView.as_view(),name='playlst_list'),
    url(r'^playlist/(?P<pk>.+)/$', PlaylistDetailView.as_view(),name='playlist_detail'),
]