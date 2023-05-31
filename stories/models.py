from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()



class Stories(models.Model):
    user = models.ForeignKey(User, related_name='story_user', unique=False,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    shoutout = models.ManyToManyField(User,verbose_name=_("Shout Out"), related_name='shoutout', blank=True)
    song = models.ForeignKey("music.Song", null=True, blank=True, verbose_name=_("Song"), on_delete=models.CASCADE)
    image = models.ImageField(upload_to=None, null=True, blank=True, height_field=None, width_field=None, max_length=100)
    viewer = models.ManyToManyField(User, verbose_name=_("Viewer"), related_name='story_viewer',unique=False,blank=True)
    active = models.BooleanField(_("Active Story"),default=True)

    class Meta: 
        default_related_name = 'stories'
        get_latest_by = 'date_created'

    def __str__(self):
        return self.user.username
        
    def __unicode__(self):
        return self.user.username