from accounts.models import MusicInteraction
from music.models import SongListener
from .serializers import LoginSerializer, RegisterSerializer, UtterlyFavouriteSerializer, MusicInteractionSerializer, RecentlyWatchedSerializer
import datetime
from Reality.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView, ListAPIView
from rest_auth.views import TokenModel
from rest_auth.app_settings import (
    TokenSerializer, create_token
)   
from rest_framework import status
from django.utils.translation import ugettext_lazy as _

from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings



class RegisterView(ListCreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    token_model = TokenModel
    queryset = TokenModel.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({'register':'successfully register'})

    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        data = TokenSerializer(user.auth_token).data
        success = {'register':'successfully register'}
        data.update(success)
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)
    
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        create_token(self.token_model, user, serializer)
        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return user


class LoginView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel
    
    
    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, _ = TokenModel.objects.get_or_create(user=self.user)


    def get_response(self):
        serializer_class = TokenSerializer

        serializer = serializer_class(instance=self.token,
                                        context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        return response


    def post(self, request, *args, **kwargs):
        self.request = request

        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})

        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()
    
class RecentlyWatchedView(ListAPIView):
    serializer_class = RecentlyWatchedSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return MusicInteraction.objects.filter(user=self.request.user).order_by('-date')[0:10]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UtterlyFavouriteView(ListAPIView):
    serializer_class = UtterlyFavouriteSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return SongListener.objects.filter(listener=self.request.user).order_by('-date_updated','-listen_count','date_listen')[0:10]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class YourTopView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MusicInteractionSerializer

    def get_queryset(self):
        return MusicInteraction.objects.filter(user=self.request.user).order_by('-song__listen_count','album__follower','song__date_listen','album__date_listen')
    

