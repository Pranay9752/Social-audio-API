from django.conf.urls import url
from django.urls import include
from .views import YourPastVibesView, WithoutTokenView, WithTokenView, HomeSView, PlaylistView, HomeFollowFeedView, ProfileView, HomeStoriesView, HomeSongView, HomeAlbumView, HomePodcastView, HomePlaylistView
urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$',ProfileView.as_view(),name='profile'),
    url(r'^h/play/$',PlaylistView.as_view(),name='play'),
    url(r'^h/withtoken/$',WithTokenView.as_view(),name='with'),
    url(r'^h/withouttoken/$',WithoutTokenView.as_view(),name='without'),
    url(r'^h/pastvibes/$',YourPastVibesView.as_view(),name='your_past_vibes'),
    url(r'^h/stories/$',HomeStoriesView.as_view(),name='recent_stories'),
    url(r'^h/story/$',HomeSView.as_view(),name='recent_story'),
    url(r'^h/songs/$',HomeSongView.as_view(),name='recent_songs'),
    url(r'^h/albums/$',HomeAlbumView.as_view(),name='recent_albums'),
    url(r'^h/podcasts/$',HomePodcastView.as_view(),name='recent_podcasts'),
    url(r'^h/playlists/$',HomePlaylistView.as_view(),name='recent_playlists'),
    url(r'^home/feed/$',HomeFollowFeedView.as_view(),name='home_feed'),
    url(r'^trending/',include('showapi.trending.urls'))
]