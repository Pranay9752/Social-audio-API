from .serializers import SongSeriaizer, AlbumSeriaizer, YourPastVibesSerializer, HomeSerializer, ProfileSerializer, HomeStoriesUserSerializer, HomeStoriesSerializer, HomeSongSeriaizer, HomeAlbumSeriaizer
from music.models import Song, Album, MusicPlayer, SongListener
from stories.models import Stories
from accounts.models import UserInteraction
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from Reality.permissions import IsOwnerOrReadOnly
from Reality.settings import baseMediaUrl
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Count

User = get_user_model()
from rest_framework.generics import GenericAPIView


from Reality.permissions import query_debugger

class WithTokenView(APIView): 
    queryset = Stories.objects.all()
    serializer_class = HomeStoriesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = {'try':'success'}
        return Response(data)

class WithoutTokenView(APIView):
    queryset = Stories.objects.all()
    serializer_class = HomeStoriesSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = {'try':'success'}
        return Response(data)

class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'
    
    def get_queryset(self):
        self.username = self.request.parser_context['kwargs']['username']
        return User.objects.annotate(
                                    following=Count('user__following',distinct=True),
                                    followers=(Count('is_follower',distinct=True)),
                                    streams=Count('songs__song_listened',distinct=True)
                ).get(username__exact=self.username)

    def userinteraction(self, request, user):
        user_recommend = user
        user = request.user
        interaction = UserInteraction.objects
        if user != user_recommend:
            if not interaction.filter(user=user,user_recommend=user_recommend).exists():
                user_point_update = interaction.create(user=user,user_recommend=user_recommend,account_points=1)
                user_point_update.save()
                return False
            else:
                user_point_update = interaction.get(user=user,user_recommend=user_recommend)
                user_point_update.account_points = user_point_update.account_points + 1
                user_point_update.save()
                return False
        return True

    def stories(self, user):
        latest=user.story_user.latest()
        stories = user.story_user.filter(active=True).values_list('id',flat=True) 
        return [latest,stories]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        song_qs = Song.objects.filter(user__username=self.username,public=True).order_by('-release_date').values('pk','name','song_image')      

        album_qs = queryset.artist.filter(public=True,playlist=False,podcast=False).order_by('-date_created').values('pk','name','album_image')
        podcast_qs = queryset.artist.filter(public=True,podcast=True).order_by('-date_created').values('pk','name','album_image')
        playlist_qs = queryset.artist.filter(public=True,playlist=True).order_by('-date_created').values('pk','name','album_image')
        story_qs = self.stories(queryset)
        
        self.userinteraction(request,queryset)

        serializer = self.get_serializer(queryset)

        stories = HomeStoriesSerializer(story_qs[0],many=False)
        song = SongSeriaizer(song_qs, many=True)
        album = AlbumSeriaizer(album_qs, many=True)
        podcast = AlbumSeriaizer(podcast_qs, many=True)
        playlist = AlbumSeriaizer(playlist_qs, many=True)

        return Response({'user':serializer.data,
                         'story':[stories.data,list(story_qs[1])],
                         'song':song.data,
                         'album':album.data,
                         'podcast':podcast.data,
                         'playlist':playlist.data
                         })



def get_following_id(self):
        return self.request.user.user.following.values_list('pk',flat=True)

class HomeStoriesView(ListAPIView):
    serializer_class = HomeStoriesUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id__in=get_following_id(self),story_user__active=True).distinct().values('username','profileImage')


class HomeSView(ListAPIView):
    queryset = Stories.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [IsAuthenticated]

    
    def get(self, request, *args, **kwargs):
        s=Stories.objects.select_related('user')
        qs = s.filter(user_id__in=get_following_id(self), active=True).order_by('-date_created').values_list('user_id',flat=True)
        data = {}
        b = []
        for obj_user in qs:
            if obj_user not in b:
                data[obj_user] = s.filter(user_id=obj_user, active=True).order_by('-date_created').values_list('pk',flat=True)
                b.append(obj_user)
        return Response(data)


class HomeSongView(ListAPIView):
    serializer_class = HomeSongSeriaizer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Song.objects.filter(user_id__in=get_following_id(self),public=True).prefetch_related('performer')

class HomeAlbumView(ListAPIView):
    serializer_class = HomeAlbumSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator_id__in=get_following_id(self), podcast=False, playlist=False,public=True)

class HomePodcastView(ListAPIView):
    serializer_class = HomeAlbumSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator_id__in=get_following_id(self), podcast=True, playlist=False,public=True)

class HomePlaylistView(ListAPIView):
    serializer_class = HomeAlbumSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator_id__in=get_following_id(self), podcast=False, playlist=True,public=True)

class PlaylistView(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = HomeAlbumSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator_id__in=get_following_id(self), podcast=False, playlist=True,public=True)


class HomeFollowFeedView(ListAPIView):
    queryset = Song.objects.all()
    serializer_class = HomeSongSeriaizer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        follower_ids = [x.pk for x in user.user.following.all()]
        song_qs = Song.objects.filter(user__id__in=follower_ids, podcast_episode=False)
        album_qs = Album.objects.filter(creator__id__in=follower_ids, podcast=True)
        querys = [song_qs,album_qs]
        for qs in querys:
            if qs == song_qs:
                songs = [{'pk': obj.pk,
                        'user_id': obj.user_id,
                        'name': obj.name,
                        'song_image': baseMediaUrl+str(obj.song_image),
                        'podcast_episode':obj.podcast_episode,
                        'cover':obj.cover,
                        'remix':obj.remix,
                        'user': obj.user.username,
                        'is_verified': obj.user.is_verified,
                        'performer': [{'username':perform.username,
                                        'profileImage':str(perform.profileImage),
                                        'is_verified':perform.is_verified} for perform in obj.performer.all()]
                        }
                        for obj in qs]
            if qs == album_qs:
                albums = [{'pk': obj.pk,
                        'creator_id': obj.creator_id,
                        'username': obj.creator.username,
                        'name': obj.name,
                        'podcast':obj.podcast,
                        'profileImage': baseMediaUrl+str(obj.creator.profileImage),
                        'album_image': baseMediaUrl+str(obj.album_image),
                        'is_verified': obj.creator.is_verified } for obj in qs]
        data = {'songs':songs,
                'albums':albums}
        return Response(data)

class YourPastVibesView(ListAPIView):
    queryset = SongListener.objects.all()
    serializer_class = YourPastVibesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return SongListener.objects.filter(listener=self.user, date_updated__lte=timezone.now() - timezone.timedelta(days=28)).order_by('-listen_count','-date_listen','date_updated')
        return SongListener.objects.filter(listener=self.user).order_by('-listen_count','-date_listen','-date_updated')

    
    def list(self, request, *args, **kwargs):
        self.user=request.user
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
