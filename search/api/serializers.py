from music.models import Trending, Song, Album
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, CharField, ImageField, BooleanField, FileField
from django.contrib.auth import get_user_model
User = get_user_model()

class TrendGenreSerializer(ModelSerializer):

    class Meta:
        model = Trending
        fields = ('id','object_id','content_type','rank')


class SongSearchSerializer(ModelSerializer):
    user = SerializerMethodField()
    class Meta:
        model = Song
        fields = ('pk','name','user','song_image')

    def get_user(self, obj):
        return obj.user.username

class AlbumSearchSerializer(ModelSerializer):
    creator = SerializerMethodField()
    class Meta:
        model = Album
        fields = ('pk','name','creator','album_image','playlist','podcast')

    def get_creator(self, obj):
        return obj.creator.username

class UserSearchSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ('pk','username','profileImage','is_verified','full_name')

class MasterSearchSerializer(Serializer):

    def to_representation(self, obj):
        if isinstance(obj, Song): 
            serializer = SongSearchSerializer(obj)
        elif isinstance(obj, Album):
            serializer = AlbumSearchSerializer(obj)
        elif isinstance(obj, User):
            serializer = UserSearchSerializer(obj)
        else:
            raise Exception("Cannot find instance!")
        return serializer.data