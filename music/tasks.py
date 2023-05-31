from __future__ import absolute_import, unicode_literals

from celery import shared_task
import datetime
from django.db.models import Count
from music.models import Song, Album, SongListener, Trending
from stories.models import Stories
from celery import shared_task
# Song.objects.filter(song_listened__date_listen__date=datetime.datetime.today() - datetime.timedelta(days=1)).annotate(numberofstreams=Count('song_listened')).order_by('-numberofstreams','-likes','-song_listened__listen_count')[:50]
@shared_task
def song_trend_update():
# Coalesce()
    # Trending.objects.all().delete()
    # songs = Song.objects.filter(sodate_listen__date=datetime.datetime.today() - datetime.timedelta(days=1)).annotate(numberofstreams=Count('song_listened')).order_by('-numberofstreams')[:50]
    # for i in range(0,len(songs)):
    #     trend_song = Trending.objects.create(content_object=songs[i],rank=i)
    #     trend_song.save()
    return None

@shared_task
def album_trend_update():
    # albums = Album.objects.filter(album_followed__date_listen__date=datetime.datetime.today() - datetime.timedelta(days=1)).annotate(numberofstreams=Count('song_listened')).order_by('-numberofstreams')[:50]
    # for i in range(0,len(albums)):
    #     trend_song = Trending.objects.create(content_object=albums[i],rank=i)
    #     trend_song.save()
    return "None"


