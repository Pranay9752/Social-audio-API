from django.contrib import admin
from django import forms
from django.contrib.admin import ModelAdmin
from .models import Song, Album, MusicPlayer, SongListener, AlbumListener, Trending

class SongCreationForm(forms.ModelForm):
       
    class Meta:
        model = Song
        fields = ('user','performer','name','genre','producer','writer','song','song_image','likes','views','explicit','cover','remix','podcast_episode')


class SongAdmin(ModelAdmin):
    readonly_fields=('likes','views','trend_points','release_date')
    # The forms to add and change user instances
    form = SongCreationForm
    add_form = SongCreationForm


    list_display = ('name','user','genre','likes','views')
    #list_filter = ('is_staff','is_admin','is_superuser')
    fieldsets = (
        ('Song', {'fields': ('name', 'genre', 'song_image','song','release_date','cover','remix')}),
        ('Type', {'fields': ('explicit','podcast_episode', 'public')}),
        ('Artists', {'fields': ('user','performer','producer','writer')}),
        ('Engagements', {'fields': ('likes','views','trend_points')})
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','performer','performer','likes','views'),
        }),
    )
    search_fields = ('name','genre','public','user')
    #ordering = ('-date_joined',)
    filter_horizontal = ()


class AlbumCreationForm(forms.ModelForm):
       
    class Meta:
        model = Album
        fields = ('creator','name','songs','album_image','podcast','likes','views', 'public', 'playlist')



class AlbumAdmin(ModelAdmin):
    readonly_fields=('likes', 'views', 'date_created')
    # The forms to add and change user instances
    form = AlbumCreationForm
    add_form = AlbumCreationForm


    list_display = ('name','creator', 'podcast', 'public', 'playlist','likes','views')
    #list_filter = ('is_staff','is_admin','is_superuser')
    fieldsets = (
        ('Album', {'fields': ('name', 'creator','date_created','album_image')}),
        ('Type', {'fields': ('podcast', 'public', 'playlist')}),
        ('Engagements', {'fields': ('likes','views')}),
        #('Activity', {'fields': ('date_joined','last_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('creator','name','songs','album_image','likes','views'),
        }),
    )
    search_fields = ('name', 'podcast', 'public', 'playlist')
    #ordering = ('-date_joined',)
    filter_horizontal = ()


class SongListenerAdmin(ModelAdmin):
    readonly_fields=('date_listen','listen_count')

    list_display = ('song','listener','date_listen')
    #list_filter = ('is_staff','is_admin','is_superuser')
    fieldsets = (
        ('Relation', {'fields': ('listener', 'song')}),
        ('Date', {'fields': ('date_listen',)}),
        ('Engagements', {'fields': ('listen_count',)})
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('song','listener','date_listen'),
        }),
    )
    search_fields = ('song','listener','date_listen')
    #ordering = ('-date_joined',)
    filter_horizontal = ()

class AlbumListenerAdmin(ModelAdmin):
    readonly_fields=('date_listen',)

    list_display = ('album','viewer','date_listen')
    #list_filter = ('is_staff','is_admin','is_superuser')
    fieldsets = (
        ('Relation', {'fields': ('album','viewer')}),
        ('Date', {'fields': ('date_listen',)}),
        ('Engagements', {'fields': ('follower',)})
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('album','viewer','date_listen'),
        }),
    )
    search_fields = ('album','viewer','date_listen')
    filter_horizontal = ()

class TrendingAdmin(ModelAdmin):
    readonly_fields=('date',)

    fieldsets = (
        ('Object', {'fields': ('object_id', 'content_type')}),
        ('Date', {'fields': ('date',)})
    )
   


admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(SongListener, SongListenerAdmin)
admin.site.register(AlbumListener, AlbumListenerAdmin)
admin.site.register(MusicPlayer)
admin.site.register(Trending, TrendingAdmin)
