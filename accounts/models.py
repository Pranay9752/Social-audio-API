
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class LowercaseCharField(models.CharField):
    """
    Override CharField to convert to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert text to lowercase.
        """
        value = super(LowercaseCharField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class UserManager(BaseUserManager):
    def _create_user(self,username, email, password, is_staff,is_admin, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        now = timezone.now()
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_admin=is_admin,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,username, email, password=None, **extra_fields):
        return self._create_user( username, email,full_name, password, False, False, False, **extra_fields)

    def create_staff(self,username, email, password, **extra_fields):
        user = self._create_user( username,email, password,  True, False, False, **extra_fields)
        user.save(using=self._db)
        return user

    def create_admin(self,username, email, password, **extra_fields):
        user = self._create_user( username,email, password,  True, True, False, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password, **extra_fields):
        user = self._create_user( username,email, password,  True, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class  User(AbstractBaseUser):

    #username = models.CharField(_('Username'), unique=True,max_length=20)
    username = LowercaseCharField(
        # Copying this from AbstractUser code
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(),],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('Email address'), unique=True, null=True, blank=True)
    email_verified = models.BooleanField(_("Email Verified"), default=False)
    phone_no = PhoneNumberField(_("Phone Number"), unique=True, null=True, blank=True)
    phone_no_verified = models.BooleanField(_("Phone Number Verified"), default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)                                                                                                                                                    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(_("Full Name"), max_length=50,null=True)
    date_of_birth = models.DateField(_("Date of birth"), auto_now=False, auto_now_add=False,null=True)
    is_verified = models.BooleanField(_("Verified"), default=False)
    profileImage = models.ImageField(_('Profile Image'),null=True, upload_to=None, height_field=None, width_field=None, max_length=100)
    gender = models.CharField(_("Gender"), max_length=6, choices=GENDER_CHOICES,null=True)
    profileTitle = models.CharField(_('Title'), max_length=20,null=True)
    profileBio = models.TextField(_('Bio'),null=True)
    profileWebsite = models.URLField(_('Website'), max_length=90,null=True)
    latitude = models.FloatField(_("Latitude"), max_length=11, default=0)
    longitude = models.FloatField(_("Longitude"), max_length=11, default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    class Meta:
        default_related_name = 'user'
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    def __str__(self):
        return self.username
    
    def natural_key(self):
        return (self.username)
    
    def __unicode__(self):
        return self.username
    
    @property
    def reputation(self):
        return len(self.is_follower.all())
    
class UserInteraction(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"),related_name='interacting', on_delete=models.CASCADE)
    user_recommend = models.ForeignKey(User, verbose_name=_("Interating with"),related_name='interacting_with', on_delete=models.CASCADE)
    stories_points = models.BigIntegerField(_("Stories Points"), default=0)
    account_points = models.BigIntegerField(_("Account Points"), default=0)
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'UserInteraction'
        verbose_name_plural = 'UserInteractions'

    def __str__(self):
        return self.user.username+' with '+self.user_recommend.username

    def __unicode__(self):
        return self.self.user_recommend.username
 
class MusicInteraction(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"),related_name='music_interaction', on_delete=models.CASCADE)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    liked = models.BooleanField(_("liked"),default=False)
    date = models.DateTimeField(auto_now_add=True) 


    class Meta:
        verbose_name = 'Music Interaction'
        verbose_name_plural = 'Music Interactions'
        default_related_name = 'music_int'
 
    def __str__(self):
        return self.user.username


def post_save_song_receiver(sender,instance,created,*args,**kwargs):
    if created == True:
        musicInteract = MusicInteraction.objects.create(user=instance.listener, content_object=instance)

post_save.connect(post_save_song_receiver,sender='music.SongListener')

def post_save_album_receiver(sender,instance,created,*args,**kwargs):
    if created == True:
        musicInteract = MusicInteraction.objects.create(user=instance.viewer, content_object=instance)
post_save.connect(post_save_album_receiver,sender='music.AlbumListener')
