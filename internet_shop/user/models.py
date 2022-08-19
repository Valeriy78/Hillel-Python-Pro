"""
User application models
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    """Custom user model implementation"""

    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = "auth_user"
        verbose_name = "user"
        verbose_name_plural = "users"
