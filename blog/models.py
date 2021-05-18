from datetime import time
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
import math

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self, **kwargs):
        return reverse('blog-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def whenposted(self):
        now = timezone.now()
        diff= now - self.date_posted
        return counttime(diff)
    
    def whenupdated(self):
        now = timezone.now()
        diff= now - self.date_updated
        return counttime(diff)
    
def counttime(diff):
    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        seconds= diff.seconds
        if seconds == 1:
            return str(seconds) +  " second ago"
        else:
            return str(seconds) + " seconds ago"
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        minutes= math.floor(diff.seconds/60)
        if minutes == 1:
            return str(minutes) + " minute ago"
        else:
            return str(minutes) + " minutes ago"
    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        hours= math.floor(diff.seconds/3600)
        if hours == 1:
            return str(hours) + " hour ago"
        else:
            return str(hours) + " hours ago"
    if diff.days >= 1 and diff.days < 30:
        days= diff.days
        if days == 1:
            return str(days) + " day ago"
        else:
            return str(days) + " days ago"
    if diff.days >= 30 and diff.days < 365:
        months= math.floor(diff.days/30)
        if months == 1:
            return str(months) + " month ago"
        else:
            return str(months) + " months ago"
    if diff.days >= 365:
        years= math.floor(diff.days/365)
        if years == 1:
            return str(years) + " year ago"
        else:
            return str(years) + " years ago"


        
    

    