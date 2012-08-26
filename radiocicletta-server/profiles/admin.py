from profiles.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'facebook', 'twitter')

admin.site.register(UserProfile, UserProfileAdmin)
