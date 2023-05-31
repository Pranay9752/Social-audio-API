from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), related_name='profile_user',on_delete=models.CASCADE)
    followers = models.ManyToManyField('followsys.Follow', verbose_name=_("Follow"),related_name='followers_detail')
    following = models.ManyToManyField('followsys.Follow', verbose_name=_("Follow"),related_name='following_detail')
    def __str__(self):
        return self.user.username

def pot_save_user_receiver(sender,instance,created,*args,**kwargs):
    if created == True:
        is_created,profile = Profile.objects.get_or_create(user=instance)
    
post_save.connect(pot_save_user_receiver,sender=User) 