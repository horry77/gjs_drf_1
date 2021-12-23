import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from image_processing import thumbnail


class Profile(models.Model):
    owner = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    nickname = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    thumb =  models.ImageField(upload_to='profile/thumbnail/', null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        #섬네일생성
        self.generate_tumbnail()
        super().save(*args,**kwargs)
    def generate_tumbnail(self):
        if self.image:
            output = thumbnail.generate_thumbnail(self.image)
            self.thumb = InMemoryUploadedFile(output,'ImageField',self.image.name,'image/jpeg',sys.getsizeof(output),None)

@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(owner=instance, nickname='임시 닉네임')