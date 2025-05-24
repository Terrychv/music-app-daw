from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('client', 'Client'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_client(self):
        return self.role == 'client'

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f'{self.username} ({self.role})'
    
# Perfil extendido con datos adicionales del usuario
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# Señales para crear y guardar el perfil automáticamente cuando se crea el usuario
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()