from rest_framework.serializers import RelatedField,Serializer, ListField, ModelSerializer, URLField, DateField, EmailField,IntegerField,CharField,ImageField,BooleanField
from accounts.api.serializers import UserSerializer
from .models import Profile
from stories.models import Stories
from music.models import Song, Album, SongListener, MusicPlayer
from followsys.models import Follow
from music.api.serializers import SongListSerializer
from accounts.models import UserInteraction
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from Reality.settings import baseMediaUrl
from Reality.permissions import query_debugger
from collections import OrderedDict

class HomeStoriesUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','profileImage')

class ProfileSerializer(ModelSerializer):
    profileImage = ImageField()
    followers = IntegerField()
    following = IntegerField()
    streams = IntegerField()

    class Meta:
        model = User
        fields = ('username','profileTitle','profileImage','full_name','is_verified','profileBio','profileWebsite','followers','following','streams')#,'stories','songs','albums','playlists','podcasts')




class HomeStoriesSerializer(ModelSerializer):
    class Meta:
        model = Stories
        fields = ('id','pk','user','song','image','date_created')


class HomeSerializer(ModelSerializer):
    #story = SerializerMethodField()
    class Meta:
        model = Stories
        fields = ('id',)
    
    #
    # def get_story(self,request):
    #     user = self.context.get("request").user
    #     # follower_ids = [x.pk for x in user.user.following.all()]
    #     # qs = Stories.objects.filter(user__id__in=follower_ids, active=True).order_by('-date_created').values_list('user__username',flat=True)
    #     # data = {}
    #     # for obj_user in qs:
    #     #     data[obj_user]=Stories.objects.filter(user__username__exact=obj_user, active=True).order_by('-date_created').values_list('pk',flat=True)
    #     return user



class SongSeriaizer(ModelSerializer):
    # user__username = RelatedField(source='user.username', read_only=True)
    class Meta:
        model = Song
        fields = ('pk','name','song_image')
        read_only_fields = fields


class AlbumSeriaizer(ModelSerializer):
    class Meta:
        model = Album
        fields = ('pk','name','album_image')

class HomeSongSeriaizer(ModelSerializer):
    class Meta:
        model = Song
        fields = ('id','pk','user','performer','name','song_image','cover','remix')

class HomeAlbumSeriaizer(ModelSerializer):
    class Meta:
        model = Album
        fields = ('id','pk','creator','name','album_image','podcast','playlist','public')


class YourPastVibesSerializer(ModelSerializer):

    class Meta:
        model = SongListener
        fields = ('pk','listener','song')
