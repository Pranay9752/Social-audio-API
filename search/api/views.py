from .serializers import TrendGenreSerializer, UserSearchSerializer, SongSearchSerializer, AlbumSearchSerializer, MasterSearchSerializer
from music.models import Trending,Song, Album
from stories.models import Stories
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from itertools import chain
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()

class TrendingGenreView(ListAPIView):
    serializer_class = TrendGenreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ['song__genre','album__songs__genre']

    def get_queryset(self):
        return Trending.objects.all().order_by('rank')

class UserSearchView(ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ['username','full_name']

    def get_queryset(self):
        return User.objects.all().order_by('-interacting_with__account_points')

class SongSearchView(ListAPIView):
    serializer_class = SongSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ['name','genre','language']

    def get_queryset(self):
        return Song.objects.filter(public=True)

class AlbumSearchView(ListAPIView):
    serializer_class = AlbumSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ['name']

    def get_queryset(self):
        return Album.objects.filter(public=True,podcast=False)

class PodcastSearchView(ListAPIView):
    serializer_class = AlbumSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    
    def get_queryset(self):
        return Album.objects.filter(public=True,podcast=True)

class MasterSearchView(ListAPIView):
    serializer_class = MasterSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('search')
        songs = Song.objects.filter(Q(name__icontains=query) | Q(genre__icontains=query) | Q(language__icontains=query),public=True)[0:7]
        albums = Album.objects.filter(public=True,name__icontains=query)[0:4]
        users = User.objects.filter(Q(username__icontains=query) | Q(full_name__icontains=query))[0:7]
        search_results = list(chain(songs, albums, users))
        search_results.sort(key=lambda x: x.reputation)
        return search_results

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
