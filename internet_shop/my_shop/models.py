"""
My_shop application models
"""

from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    """Category model implementation"""

    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Product model implementation"""

    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("product", kwargs={"slug": self.slug})

    def decrease_quantity(self, number):
        if number <= self.quantity:
            self.quantity -= number
        else:
            raise ValueError("Quantity can not be negative")
        self.save()

    def increase_quantity(self, number):
        self.quantity += number
        self.save()
