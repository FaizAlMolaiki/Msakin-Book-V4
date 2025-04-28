from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default/default_avatar.png')
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture and not self.profile_picture.name.endswith('default_avatar.png'):
            img = Image.open(self.profile_picture.path)
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg

            # Make square
            size = min(img.size)
            left = (img.width - size) // 2
            top = (img.height - size) // 2
            right = left + size
            bottom = top + size
            img = img.crop((left, top, right, bottom))

            # Resize
            if size > 300:
                img = img.resize((300, 300), Image.Resampling.LANCZOS)

            # Save
            img.save(self.profile_picture.path, quality=90, optimize=True)

    @property
    def avatar_url(self):
        """Return the URL of the avatar, using default if none exists"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/accounts/default/default_avatar.png'

    @property
    def name(self):
        """Return the full name of the user, or username if no name is set"""
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or self.user.username

    @property
    def first_name(self):
        """Return the first name of the user"""
        return self.user.first_name

    @property
    def last_name(self):
        """Return the last name of the user"""
        return self.user.last_name

    @property
    def email(self):
        """Return the email of the user"""
        return self.user.email

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

class SocialAccount(models.Model):
    PROVIDER_CHOICES = (
        ('google', 'Google'),
        ('apple', 'Apple'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'provider_id')

    def __str__(self):
        return f'{self.user.username} - {self.provider}'
