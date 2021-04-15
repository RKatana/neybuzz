from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.
class Hood(models.Model):
    user = models.ForeignKey('Profile', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, null=True)
    description = models.CharField(max_length=400, null=True)
    location = models.CharField(max_length=200, null=True)
    population = models.IntegerField()
    image = CloudinaryField('image')

    def __str__(self):
        return self.name
    
    def create_hood(self):
        self.save()

    def delete_hood(self):
        self.delete()

    @classmethod
    def find_hood(cls, id):
        hood = cls.objects.get(id = id)
        return hood

    def update_hood(self, name):
        self.name = name
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=300, blank=True)
    image = CloudinaryField('image')
    neighborhood = models.ForeignKey(Hood, on_delete=models.SET_NULL, null=True, related_name='users')

    def __str__(self):
        return f'{self.user.username} profile'

class Business(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=60, null=True)
    description = models.CharField(max_length=400, null=True)
    neighborhood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image')

    def __str__(self):
        return self.title

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user = instance)