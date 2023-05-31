from django.conf.urls import url
from django.urls import path
from .views import StoryCreateView,StoriesDetailView,UserStoriesView
urlpatterns = [
    url(r'^stories/create/$', StoryCreateView.as_view(),name='create_stories'),
    url(r'^(?P<user__username>[\w-]+)/stories/(?P<pk>\d+)/$', StoriesDetailView.as_view(),name='stories_detail'),
    url(r'^(?P<username>[\w-]+)/stories/$', UserStoriesView.as_view(),name='user_stories')
]