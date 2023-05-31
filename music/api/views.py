from rest_framework import generics
from music.commands import commandOperation
from music.models import  Song,Album
from .serializers import SongSerializer,SongListSerializer,AlbumSerializer,AlbumListSerializer, AlbumSongSerializer
from Reality.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

'''    song    '''
class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data['user'] = str(request.user.id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AllSongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongListSerializer
    permission_classes = [IsAuthenticated]    
    
class SongListView(generics.ListAPIView):
    serializer_class = SongListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Song.objects.filter(user=self.request.user)
    
    
class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        if request.data['user'] == str(request.user.id):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            raise PermissionDenied('You are not authorized to do this action')
    

'''    album    '''
class AlbumCreateView(generics.CreateAPIView):
    queryset = Album.objects.filter(podcast=False, playlist=False)
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data['creator'] = str(request.user.id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AllAlbumListView(generics.ListAPIView):
    queryset = Album.objects.filter(podcast=False, playlist=False)
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]    

class AlbumListView(generics.ListAPIView):
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator=self.request.user, podcast=False, playlist=False)
    

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.filter(podcast=False, playlist=False)
    serializer_class = AlbumSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'
    

    def update(self, request, *args, **kwargs):
        if request.data['creator'] == str(request.user.id):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            raise PermissionDenied('not authorized')

class AlbumSongView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = AlbumSongSerializer

    def post(self, request, *args, **kwargs):
        self.request = request

        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})

        self.serializer.is_valid(raise_exception=True)

        album_id = self.serializer.validated_data['album_id']
        songentry = self.serializer.validated_data['songentry']
        response = commandOperation([int(album_id),songentry], request.user)
        
        return Response(response)
    


''' Podcast'''
class AllPodcastListView(generics.ListAPIView):
    queryset = Album.objects.filter(podcast=True, playlist=False)
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]    
    
class PodcastListView(generics.ListAPIView):
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator=self.request.user, podcast=True, playlist=False)
    
    
class PodcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.filter(podcast=True, playlist=False)
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    lookup_field = 'pk'
    

    def update(self, request, *args, **kwargs):
        if request.data['creator'] == str(request.user.id):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            raise PermissionDenied('not authorized')

'''    playlist    '''
class AllPlaylistListView(generics.ListAPIView):
    queryset = Album.objects.filter(podcast=False, playlist=True)
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]    
    
class PlaylistListView(generics.ListAPIView):
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(creator=self.request.user, podcast=False, playlist=True)
    
    
class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.filter(podcast=False, playlist=True)
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    lookup_field = 'pk'
    

    def update(self, request, *args, **kwargs):
        if request.data['creator'] == str(request.user.id):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            raise PermissionDenied('not authorized')



