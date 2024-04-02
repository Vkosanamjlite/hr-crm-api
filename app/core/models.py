import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.conf import settings


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a user"""
        if not email:
            raise ValueError('Users must have an email address')
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = str(uuid.uuid4())
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = str(uuid.uuid4())
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Recipe(models.Model):
    """ Recipe model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Email(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='emails',
        on_delete=models.CASCADE)
    email = models.EmailField()


class PhoneNumber(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='phone_numbers',
        on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)


class SocialMediaLink(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='social_media_links',
        on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=100)
    link = models.URLField()
    tag = models.CharField(max_length=100)
