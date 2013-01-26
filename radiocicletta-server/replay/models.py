from django.db import models

class Replay(models.Model):
    date = models.DateTimeField(blank=False)
    description = models.TextField(blank=True)
