
from django.contrib.auth import get_user_model
from accounts.models import UserInteraction, MusicInteraction
from django.contrib.auth.models import Group
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
User=get_user_model()



class UserCreationForm(forms.ModelForm):
   
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ('email','username','password','full_name','date_of_birth','gender','is_verified','profileImage','profileTitle','profileBio','profileWebsite')



    def save(self, commit=True):
        # Save the provided password1 in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    #password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','username','password','full_name','date_of_birth','gender','profileImage','profileTitle','profileBio','profileWebsite','is_verified','is_active', 'is_admin','is_superuser')

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password


class UserAdmin(BaseUserAdmin):
    readonly_fields=('date_joined','last_login','password')
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ('username','email','full_name','date_of_birth','gender','is_verified')
    list_filter = ('is_staff','is_admin','is_superuser')
    fieldsets = (
        (None, {'fields': ('email','phone_no', 'password')}),
        ('Personal info', {'fields': ('username','full_name','date_of_birth','profileImage','profileTitle','profileBio','profileWebsite','is_verified')}),
        ('Permissions', {'fields': ('is_staff','is_admin','is_superuser','email_verified','phone_no_verified',)}),
        ('Activity', {'fields': ('latitude','longitude','date_joined','last_login')}),
    ) 
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password'),
        }),
    )
    search_fields = ('username',)
    ordering = ('-date_joined',)
    filter_horizontal = ()


#Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(UserInteraction)
admin.site.register(MusicInteraction)

# unregister the Group model from admin.
admin.site.unregister(Group)