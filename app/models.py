"""
Definition of models.
"""

from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.sessions.models import Session

# Create your models here.
class Event(models.Model):
    title =  models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    added_at = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    session_key = models.ForeignKey(Session, blank=True)


class Confirmation(models.Model):
    session_key = models.ForeignKey(Session)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
