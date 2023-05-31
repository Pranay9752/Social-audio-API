from stories.models import Stories
from music.models import Song
from accounts.models import UserInteraction
from music.api.serializers import ExtraListInfo
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import get_user_model
from Reality.settings import baseMediaUrl
from Reality.permissions import query_debugger
User = get_user_model()

class StorySerializer(ModelSerializer):
    story_id = SerializerMethodField()

    class Meta:
        model = Stories
        fields = ('story_id',)

    def get_story_id(self,request):
        data = Stories.objects.filter(user__pk=request.pk, active=True).order_by('-date_created').values_list('pk',flat=True)
        return data

class StoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Stories
        fields = ('id','pk','user','song','image','shoutout','viewer')

class StoryRetrieveSerializer(ModelSerializer):
    user = SerializerMethodField()
    shoutout = SerializerMethodField()
    viewer = SerializerMethodField()

    class Meta:
        model = Stories
        fields = ('id','pk','user','song','image','shoutout','viewer')

    def storyinteraction(self, request, *args, **kwargs):
        user_recommend = request.user
        user = self.context.get("request").user
        interaction = UserInteraction.objects
        if user != user_recommend:
            if not interaction.filter(user=user,user_recommend=user_recommend).exists():
                user_point_update = interaction.create(user=user,user_recommend=user_recommend,stories_points=1)
                user_point_update.save()
                return None
            else:
                user_point_update = interaction.get(user=user,user_recommend=user_recommend)
                user_point_update.stories_points = user_point_update.stories_points + 1
                user_point_update.save()
                return None

        return None

    def get_user(self,request):

        self.storyinteraction(request)

        obj = Stories.objects.select_related("user").get(id=request.pk)#.values_list('pk','user__id','user__username','user__profileImage','user__is_verified')
        data =  {'pk': obj.user.pk,
                 'user_id': obj.user.id,
                 'username': obj.user.username,
                 'profileImage': baseMediaUrl+str(obj.user.profileImage),
                 'is_verified': obj.user.is_verified,
                }
        return data

    
    def get_shoutout(self,request):
        obj = Stories.objects.get(id=request.pk).shoutout.all()#.prefetch_related("shoutout")
        data = [{'username':user.username,
                 'pk':user.pk,
                 'user_id':user.id,
                 'profileImage':baseMediaUrl+str(user.profileImage),
                 'is_verified':user.is_verified} for user in obj],
                #  'song': {'song_pk':obj.song,
                #           'song':baseMediaUrl+str(obj.song.song),
                #           'song_name':obj.song.name,
                #           'song_image':baseMediaUrl+str(obj.song.song_image),
                #           'performer': [{'username':perform.username,
                #                         'profileImage':baseMediaUrl+str(perform.profileImage),
                #                         'is_verified':perform.is_verified} for perform in obj.song.performer.all()]},
        return data

    def get_viewer(self,request):
        obj = Stories.objects.get(id=request.pk).viewer.all()
        data = [{'username':user.username,
                'pk':user.pk,
                'user_id':user.id,
                'profileImage':baseMediaUrl+str(user.profileImage),
                'is_verified':user.is_verified} for user in obj], 
        return data

