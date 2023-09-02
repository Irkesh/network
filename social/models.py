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

    def send_friend_request(self, to_user):
        FriendsLink.objects.create(from_user=self, to_user=to_user)
    
    def accept_friend_request(self, from_user):
        friends_link = FriendsLink.objects.get(from_user=from_user, to_user=self)
        friends_link.delete()  # You might want to modify this logic based on your needs
        self.friends.add(from_user)
        from_user.friends.add(self)

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

class StatusUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Status Update"


class FriendsLink(models.Model):
    
    from_user = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name='friend_requests_sent')
    to_user = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name='friend_requests_received')
    established_at = models.DateTimeField(auto_now_add=True)
   
