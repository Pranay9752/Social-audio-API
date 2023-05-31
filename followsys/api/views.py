from .serializers import FollowingCreateSerializer, FollowerSerializer, FollowingSerializer, Serializer
from followsys.models import Follow
from Reality.permissions import IsOwnerOrReadOnly
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
User=get_user_model() 

class FollowingView(RetrieveAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'user__username'

class FollowerView(RetrieveAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

class FollowingCreateView(GenericAPIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = Serializer
    
    def put(self, request, *args, **kwargs):
        self.request = request
        request_user = self.request.user.pk
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})

        self.serializer.is_valid(raise_exception=True)
        try:
            f_user = self.serializer.data['follow_id']
            if str(f_user) == str(request_user):
                return Response("cannot follow yourself")

            obj = User.objects.select_related('user')
            user = obj.get(pk=request_user).user.following
            following = obj.get(pk=f_user)

            if following in user.all():
                user.remove(following)
                return Response('user added')

            else:
                user.add(following)
                return Response('user removed')

        except:
            return Response("user not found")