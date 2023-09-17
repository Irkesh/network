from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class AppUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    organisation = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)

    def get_user_id(self):
        return self.user.pk

    def __str__(self):
        return self.user.username

class Image(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    image = models.FileField(blank=False)    
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Status(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s Status Update"


    
class Friendship(models.Model):
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')])
    established_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.status}"
    
   
