from django.contrib import admin
from django import forms
from django.contrib.admin import ModelAdmin
from .models import Stories

class StoriesCreationForm(forms.ModelForm):
       
    class Meta:
        model = Stories
        fields = ('user','song','image','shoutout')



class StoriesAdmin(ModelAdmin):
    readonly_fields=('date_created',)
    # The forms to add and change user instances
    form = StoriesCreationForm
    add_form = StoriesCreationForm


    list_display = ('user','song','date_created')
    #list_filter = ('is_staff','is_admin','is_superuser')
    fieldsets = (
        ('Story', {'fields': ('user', 'date_created','image')}),
        ('Type', {'fields': ('active',)}),
        ('Songs', {'fields': ('song',)}),
        ('Engagements', {'fields': ('shoutout','viewer')}),
        #('Activity', {'fields': ('date_joined','last_login')}),
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','pk','user','song','image','shoutout','viewer','date_created'),
        }),
    )
    search_fields = ('id','pk','user','song')
    #ordering = ('-date_joined',)
    filter_horizontal = ()

admin.site.register(Stories, StoriesAdmin)