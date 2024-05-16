from django.db import models
from django.conf import settings

class Chiste(models.Model):
    texto = models.TextField()
    autor = models.CharField(max_length=255, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joke = models.ForeignKey('jokes.Chiste', related_name='votes', on_delete=models.CASCADE)

