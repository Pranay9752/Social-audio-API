from .serializers import TrendingStoriesSerializer, TrendingSeriaizer
from music.models import Song, Album, SongListener, Trending
from stories.models import Stories
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from Reality.permissions import IsOwnerOrReadOnly
from Reality.settings import baseMediaUrl
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from Reality.permissions import query_debugger
#Song.objects.annotate(num_books=Count('song_listened'))
class TrendingStoriesView(ListAPIView):
    queryset = Stories.objects.all()
    serializer_class = TrendingStoriesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        qs = Stories.objects.all()
        data = []
        ids = []
        for obj in qs:
           if obj.user_id not in ids:
                info =  {'pk': obj.pk,
                        'user_id': obj.user_id,
                        'username': obj.user.username,
                        'profileImage': baseMediaUrl+str(obj.user.profileImage),
                        'is_verified': obj.user.is_verified,
                        'image':baseMediaUrl+str(obj.image) }
                data.append(info) 
                ids.append(obj.user_id)
        return Response(data)

class TrendingSongView(ListAPIView):
    serializer_class = TrendingSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trending.objects.filter(song__podcast_episode=False)

class TrendingAlbumView(ListAPIView):
    serializer_class = TrendingSeriaizer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trending.objects.filter(album__podcast=False, album__playlist=False, album__public=True)
    
class TrendingPodcastView(ListAPIView):
    serializer_class = TrendingSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trending.objects.filter(album__podcast=True, album__playlist=False, album__public=True)

class TrendingPlaylistView(ListAPIView):
    serializer_class = TrendingSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trending.objects.filter(album__podcast=False, album__playlist=True, album__public=True)
    
