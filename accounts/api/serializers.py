from accounts.models import MusicInteraction, GENDER_CHOICES
from music.models import Song, Album

from django.conf import settings
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists, get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(required=True, write_only=True,
                                       style={'input_type':'password'}
    )
    full_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    is_verified = serializers.BooleanField(default=False, read_only=True)
    gender = serializers.ChoiceField(GENDER_CHOICES,required=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if (datetime.date.today() - data['date_of_birth']) < datetime.timedelta(days=11*365):
            raise serializers.ValidationError(_("Your age does not satisfy our terms."))
        return data

    # def custom_signup(self):
    #     pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'is_veriied': self.validated_data.get('is_verified', ''),
            'gender': self.validated_data.get('gender', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.full_name = self.cleaned_data['full_name']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.is_veriied = self.cleaned_data['is_veriied']
        user.gender = self.cleaned_data['gender']
        adapter.save_user(request, user, self)
        #self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user                                                                                                                                                                                                       

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    # def authenticate(self, **kwargs):
    #     return authenticate(self.context['request'], **kwargs)

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise ValidationError(msg)

        return user

    def validate(self, attrs):

        data = dict(attrs)
        
        # username = attrs.get('username')
        # password = attrs.get('password')

        user = self._validate_username(dict(attrs)['username'], dict(attrs)['password'])

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        attrs['user'] = user

        return attrs

class UserDetailAndEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','username', 'email','phone_no','full_name','date_of_birth','gender','is_verified','profileImage','profileTitle','profileBio','latitude','longitude','email_verified','phone_no_verified','profileWebsite')
        read_only_fields = ('email','is_verified','date_of_birth')


class UserSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','username')
        read_only_fields = fields

   
class MusicInteractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MusicInteraction
        fields = ['content_type','object_id']

class SongSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = ('pk','name','user','song_image')

    def get_user(self, obj):
        return obj.user.username

class AlbumSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    class Meta:
        model = Album
        fields = ('pk','name','creator','album_image','playlist','podcast')

    def get_creator(self, obj):
        return obj.creator.username

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('pk','username','profileImage','is_verified','full_name')

class RecentlyWatchedSerializer(serializers.Serializer):

    def to_representation(self, obj):
        obj = obj.content_object
        if isinstance(obj, Song): 
            serializer = SongSerializer(obj)
        elif isinstance(obj, Album):
            serializer = AlbumSerializer(obj)
        elif isinstance(obj, User):
            serializer = UserSerializer(obj)
        else:
            raise Exception("Cannot find instance!")
        return serializer.data

class UtterlyFavouriteSerializer(serializers.Serializer):

    def to_representation(self, obj):
        serializer = SongSerializer(obj.song)
        return serializer.data