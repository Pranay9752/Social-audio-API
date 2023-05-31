from rest_framework.serializers import ModelSerializer
from stories.models import Stories
from music.models import Song, Album, Trending


class TrendingStoriesSerializer(ModelSerializer):
    class Meta:
        model = Stories
        fields = ('id','pk','user','song','image')

class TrendingSeriaizer(ModelSerializer):
    class Meta:
        model = Trending
        fields = ['content_type','object_id']

