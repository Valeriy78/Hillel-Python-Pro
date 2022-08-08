from django.db import models


class Category(models.Model):
    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=64)
    description = models.TextField()


class Product(models.Model):
    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
