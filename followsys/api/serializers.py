from followsys.models import Follow
from rest_framework.serializers import Serializer,ModelSerializer,SerializerMethodField,StringRelatedField,ImageField,CharField,BooleanField,PrimaryKeyRelatedField
from django.contrib.auth import get_user_model
User = get_user_model()
from Reality.settings import baseMediaUrl

class FollowerSerializer(ModelSerializer):
    followers = SerializerMethodField()
    class Meta:
        model = Follow
        fields = ('followers',)
    
    
    def get_followers(self, obj):
        qs = self.context.get("request").user.is_follower.prefetch_related('user')

        data = [{'id': obj.pk,
                 'user_id': obj.user_id,
                 'username': obj.user.username, 
                 'profileImage': baseMediaUrl+str(obj.user.profileImage),
                 'profileTitle': obj.user.profileTitle,
                 'is_verified': obj.user.is_verified } for obj in qs]
        return data
        
class FollowingSerializer(ModelSerializer):
    following = SerializerMethodField()
    class Meta:
        model = Follow
        fields = ('following',)
    
    
    def get_following(self, obj):
        qs = self.context.get("request").user.user.following.prefetch_related('user')

        data = [{'id': obj.pk,
                 'user_id': obj.user.user_id,
                 'username': obj.username, 
                 'profileImage': baseMediaUrl+str(obj.profileImage),
                 'profileTitle': obj.profileTitle,
                 'is_verified': obj.is_verified } for obj in qs]
        return data


class FollowingCreateSerializer(ModelSerializer):
    
    class Meta:
        model = Follow
        fields = ('user','following')



class Serializer(Serializer):
    follow_id = CharField(required=True, allow_blank=False)


    def validate(self, attrs):

        data = dict(attrs)

        follow_id = attrs.get('follow_id')

        return attrs
