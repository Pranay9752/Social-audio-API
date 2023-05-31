from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User = get_user_model()


class Follow(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"),related_name="user" ,on_delete=models.CASCADE) 
    ''' to obtain user ' eeee = User.objects.first() , eeee.user'    '''          
    following = models.ManyToManyField(User, verbose_name=_("Following"),related_name='is_follower',blank=True)   
    ''' to obtain followers   ' eeee.is_follower.all()'   '''
    ''' to obtain following   ' eeee.user.following.all()'   '''
    relation_formed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

def pot_save_user_receiver(sender,instance,created,*args,**kwargs):
    if created == True:
        is_created,follow = Follow.objects.get_or_create(user=instance)
    
post_save.connect(pot_save_user_receiver,sender=User)
