import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *
from .models import AppUser, Image, Status, Friendship


class AppUserModelTestCase(TestCase):
    def test_str_representation(self):
        user = User.objects.create(username='testuser')
        app_user = AppUser.objects.create(user=user)
        self.assertEqual(str(app_user), 'testuser')


class ImageModelTestCase(TestCase):
    def test_str_representation(self):
        user = User.objects.create(username='testuser')
        app_user = AppUser.objects.create(user=user)
        image = Image.objects.create(name='test_image', image='test_image.png', user=app_user)
        self.assertEqual(str(image), 'test_image')

class StatusModelTestCase(TestCase):
    def test_str_representation(self):
        user = User.objects.create(username='testuser')
        app_user = AppUser.objects.create(user=user)
        status = Status.objects.create(user=app_user, content='Test status')
        self.assertEqual(str(status), "testuser's Status Update")

class FriendshipModelTestCase(TestCase):
    def test_str_representation(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        app_user1 = AppUser.objects.create(user=user1)
        app_user2 = AppUser.objects.create(user=user2)
        friendship = Friendship.objects.create(sender=app_user1, receiver=app_user2, status='pending')
        self.assertEqual(str(friendship), 'user1 to user2: pending')


