from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
UserModel = get_user_model()
Genres = ( ('Blues','Blues'), 
           ('Jazz','Jazz'),
           ('Rhythm and Blues','Rhythm and Blues'),
           ('Rock and Roll','Rock and Roll'),
           ('Rock','Rock'), 
           ('Country','Country'),
           ('Soul','Soul'),
           ('Dance','Dance'),
           ('Hip Hop','Hip Hop'),
           ('Heavy Metal','Heavy Metal'),
           ('Pop','Pop'),
           ('Latin','Latin'),
           ('Folk','Folk'),
           ('House','House'),
           ('Electronic','Electronic'), 
           ('Comedy','Comedy'),
           ('Instrumental','Instrumental'),
           ('Avant-garde','Avant-garde'),
           ('Music','Music'),
           ('TV & Movies','TV & Movies'),
           ('Comedy','Comedy'),
           ('Technology','Technology'),
           ('Kids & Family','Kids & Family'),
           ('Science','Science'),
           ('Health & Living','Health & Living'),
           ('Arts','Arts'),
           ('Business','Business'),
           ('Religion & Spirituality','Religion & Spirituality'),
           ('Sports','Sports'),
           ('Hobbies & games','Hobbies & games'),
           ('News & Politics','News & Politics'),
           ('Society & Culture','Society & Culture'))

Languages = (('English','English'),)

class Trending(models.Model):
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    rank = models.IntegerField(_("Rank"),default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Trending {}'.format(self.rank)#+self.date.strftime("%d-%m-%Y")

class Song(models.Model):
    user = models.ForeignKey(UserModel, related_name='songs', unique=False,on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50)
    song = models.FileField(_("Song"), upload_to=None, max_length=100)
    genre = MultiSelectField(choices=Genres)
    language = MultiSelectField(choices=Languages)
    place = models.CharField(_("Place"), max_length=50)
    song_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    likes = models.IntegerField(_("likes"),default=0)
    views = models.IntegerField(_("likes"),default=0)
    trend_points = models.IntegerField(_("Trend Points"),default=0)
    performer = models.ManyToManyField(UserModel,verbose_name=_("Performed By"),related_name='artist_in_song',unique=False,blank=True)
    producer = models.ManyToManyField(UserModel, verbose_name=_("Produced By"), related_name='producer_of_song',unique=False,blank=True)
    writer = models.ManyToManyField(UserModel, verbose_name=_("written By"), related_name='writer_of_song',unique=False,blank=True)
    listeners = models.ManyToManyField(UserModel, verbose_name=_("Listeners"), related_name='song_listeners',through='SongListener')
    release_date = models.DateTimeField(auto_now_add=True)
    explicit = models.BooleanField(_("Explicit Content"),default=False)
    remix = models.BooleanField(_("Remix song"),default=False)
    cover = models.BooleanField(_("Cover song"),default=False)
    public = models.BooleanField(_("Public"), default=False)
    podcast_episode = models.BooleanField(_("Podcast Episode"),default=False)

    trending_songs = GenericRelation(Trending, related_query_name='song')
    
    def __str__(self):
        return self.name #+' - ' + self.user.username

    def __unicode__(self):
        return self.performer.username or self.producer.username or self.writer.username

    @property
    def reputation(self):
        return len(self.listeners.all())

class SongListener(models.Model):
    listener = models.ForeignKey(UserModel, related_name='listener', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='song_listened', on_delete=models.CASCADE)
    date_listen = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    listen_count = models.IntegerField(_("Listen Count"),default=0)
    
    music_interacton = GenericRelation('accounts.MusicInteraction', related_query_name='song')


    def __str__(self):
        return self.listener.username +' has listened ' + self.song.name



class Album(models.Model):
    songs =  models.ManyToManyField("music.Song", verbose_name=_("Songs"), related_name='songs',unique=False)
    creator = models.ForeignKey(UserModel, verbose_name=_("Creator"),related_name='artist', on_delete=models.CASCADE)
    name = models.CharField(_("Album Name"), max_length=50)
    album_image = models.ImageField(upload_to=None, null=True, height_field=None, width_field=None, max_length=100)
    likes = models.IntegerField(_("Likes"),default=0)
    views = models.IntegerField(_("Views"),default=0)
    followers = models.ManyToManyField(UserModel, verbose_name=_("Listeners"), related_name='album_followers',through='AlbumListener')
    date_created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(_("Public"), default=False)
    playlist = models.BooleanField(_("Playlist"), default=False)
    podcast = models.BooleanField(_("Podcast"),default=False)
    
    trending_albums = GenericRelation(Trending, related_query_name='album')

    def __str__(self):
        return self.name +' by '+self.creator.username

    def user(self):
        return self.creator.username

    @property
    def reputation(self):
        return self.followers.count()

class AlbumData(models.Model):
    album = models.ForeignKey(Album, verbose_name=_("Album"), on_delete=models.CASCADE)
    song = models.ForeignKey(Song, verbose_name=_("Song in Album"), on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("AlbumData")
        verbose_name_plural = _("AlbumDatas")

 

class AlbumListener(models.Model):
    viewer = models.ForeignKey(UserModel, related_name='album_follower', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='album_followed', on_delete=models.CASCADE)
    date_listen = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    music_interacton = GenericRelation('accounts.MusicInteraction', related_query_name='album')

    def __str__(self):
        return self.viewer.username +' has listened ' + self.album.name


class MusicPlayer(models.Model):
    user = models.OneToOneField(UserModel, verbose_name=_("User"),unique=False, on_delete=models.CASCADE)
    songs = models.ManyToManyField("music.Song", blank=True, verbose_name=_("songs"))

    def __str__(self):
        return self.user.username+' music-player'


def post_save_user_receiver(sender,instance,created,*args,**kwargs):
    if created:
        is_created,music = MusicPlayer.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver,sender=UserModel)
