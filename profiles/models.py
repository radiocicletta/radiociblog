from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=50, blank=True, unique=True)
    appear_as_nickname = models.BooleanField(default=False,
                                             help_text='Il tuo nickname sar&agrave; visualizzato al posto del nome')
    blog = models.URLField("Blog", blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
