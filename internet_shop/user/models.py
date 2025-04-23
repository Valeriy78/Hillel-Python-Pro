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
    money = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)

    class Meta:
        db_table = "auth_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def add_money(self, amount):
        """Adds an amount of money to the user account"""

        self.money += amount
        self.save()

    def get_money(self, amount):
        """Takes an amount of money from the user account"""

        if self.money >= amount:
            self.money -= amount
        else:
            raise ValueError("There is not enough money")
        self.save()
        return amount
