"""
Purchase application models
"""

from django.db import models

from user.models import UserModel
from my_shop.models import Product


class Cart(models.Model):
    """
    Shopping cart implementation. Every user (except for the staff) can have many carts, but only one
    is actual. User can add products to the actual cart. After confirmation of the purchase, current cart
    becomes inactual.
    """

    customer = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="carts")
    is_actual = models.BooleanField(default=True)

    def calculate_sum(self):
        """Returns the total cost of products in the cart"""
        total_sum = 0
        items = self.items.all()
        for item in items:
            price = item.product.price
            quantity = item.quantity
            total_sum += price * quantity
        return total_sum

    def make_inactual(self):
        """Makes the cart inactual"""
        self.is_actual = False
        self.save()


class CartItem(models.Model):
    """Item in the shopping cart implementation"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.product.name


class Order(models.Model):
    """User's order implementation"""

    PURCHASE_STATUS_CHOICES = (
        ('IN PROCESSING', 'In processing'),
        ('CANCELLED', 'Cancelled'),
        ('DONE', 'Done')
    )
    customer = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="orders")
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=13, choices=PURCHASE_STATUS_CHOICES, default='IN PROCESSING')

    def __str__(self):
        return f"Order № {self.id}"

    def cancel(self):
        self.status = 'CANCELLED'
        self.save()


class OrderReturn(models.Model):
    """User's order return implementation"""

    customer = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for the order return  № {self.id}"

    def confirm(self):
        self.status = True
        self.save()
