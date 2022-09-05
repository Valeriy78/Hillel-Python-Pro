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

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("product", kwargs={"slug": self.slug})
