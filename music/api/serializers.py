from music.models import Song, Album
from rest_framework.serializers import ModelSerializer, CharField, ImageField, BooleanField, Serializer
from django.contrib.auth import get_user_model
User = get_user_model()

class ExtraListInfo(ModelSerializer):
    user_username = CharField(source='username')
    profile_image = ImageField(source='profileImage')
    verified = BooleanField(source='is_verified')
    class Meta:
        model = Song
        fields = ('user_username','profile_image','verified')


# Song
class SongSerializer(ModelSerializer):

    class Meta:
        model = Song
        fields = ('id','user','performer','name','genre','producer','writer','song','cover','remix','podcast_episode','song_image','likes','views')
        read_only_fields = ('likes','views')


class SongListSerializer(ModelSerializer):
    producer = ExtraListInfo(many=True)
    writer = ExtraListInfo(many=True)
    performer = ExtraListInfo(many=True)
    user = ExtraListInfo(many=False)
    class Meta:
        model = Song
        fields = ('id','pk','user','performer','name','genre','producer','writer','song','song_image','podcast_episode','likes','views','cover','remix')
        read_only_fields = ('likes','views')


# Album
class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = ('id','creator','name','songs','album_image','podcast','public','playlist','likes','views')
        read_only_fields = ('likes','views')


class AlbumListSerializer(ModelSerializer):
    songs = SongListSerializer(many=True)    
    creator = ExtraListInfo(many=False)

    class Meta:
        model = Album
        fields = ('id','creator','name','songs','album_image','podcast','public','playlist','likes','views')
        read_only_fields = ('likes','views')


class AlbumSongSerializer(Serializer):
    album_id = CharField(required=False, allow_blank=False)
    songentry = CharField(required=False, allow_blank=False)

