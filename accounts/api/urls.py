from allauth.account.views import confirm_email
from django.conf.urls import url
from django.urls import path, include
from .views import RegisterView, LoginView, RecentlyWatchedView, UtterlyFavouriteView, YourTopView
urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls')),
    url(r'^auth/', include('allauth.urls')),
    url(r'^registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^recently-watched/$', RecentlyWatchedView.as_view(), name='recently_watched'),
    url(r'^utterly-favourite/$', UtterlyFavouriteView.as_view(), name='utterly_favourite'),
    url(r'^your-top/$', YourTopView.as_view(), name='your_top'),
]