from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Administrator'),
        ('client', 'CLient'),
    ]

    name = models.CharField(max_length = 255)

    role = models.CharField(max_length = 10, choices = ROLES)

    # The following is used to avoid clashes with 
    # the basic user proviede by django
    # Provide a group and permissions for the user
    groups = models.ManyToManyField (
        'auth.Group',
        related_name = 'custom_user_groups',
        blank = True,
        help_text = 'The group the user belongs to with the provided permissions',
        verbose_name = 'groups',
    )

    user_permissions = models.ManyToManyField (
        'auth.Permission',
        related_name = 'custom_user_permissions',
        blank = True,
        help_text = 'Specific permissions for this user',
        verbose_name = 'user permissions',
    )


