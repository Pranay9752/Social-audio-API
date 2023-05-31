from .views import FollowingCreateView, FollowerView, FollowingView
from django.urls import path
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<user__username>[\w-]+)/followers/$',FollowerView.as_view(),name='followers'),
    url(r'^(?P<user__username>[\w-]+)/following/$',FollowingView.as_view(),name='following'),
    url(r'^following/edit/$',FollowingCreateView.as_view(),name='edit_following'),
]