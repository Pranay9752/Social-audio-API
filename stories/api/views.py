from rest_framework import generics
from stories.models import  Stories
from .serializers import StorySerializer, StoryCreateSerializer, StoryRetrieveSerializer
from Reality.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

'''    story    '''
class StoryCreateView(generics.CreateAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoryCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data['user'] = str(request.user.id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class StoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoryRetrieveSerializer
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
            raise PermissionDenied('not authorized for this actions')

class UserStoriesView(generics.RetrieveAPIView):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()

