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
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=13, choices=PURCHASE_STATUS_CHOICES, default='IN PROCESSING')

    def __str__(self):
        return f"Order № {self.id}"

    def cancel(self):
        self.status = 'CANCELLED'
        self.save()

    def save(self, **kwargs):
        """
        After the purchase confirmation:
        1. Calculates the total cost of products.
        2. Gets from the user's account an amount of money equal to the total cost.
        3. Diminishes the quantity of products that have been purchased.
        4. Current user's cart becomes inactual.
        5. Creates new actual cart for the user.
        6. Creates new order object.
        """

        if not self.id:
            cart = self.cart
            customer = self.cart.customer
            cart_items = cart.items.all()

            total_cost = cart.calculate_sum()
            customer.get_money(total_cost)

            for item in cart_items:
                product = item.product
                quantity = item.quantity
                product.decrease_quantity(quantity)

            cart.make_inactual()
            new_cart = Cart(customer=customer)
            new_cart.save()

        super().save(**kwargs)


class OrderReturn(models.Model):
    """User's order return implementation"""

    CHOICES = [('CONFIRM', 'confirm'),
               ('REJECT', 'reject')]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for the order return  № {self.id}"

    def confirm(self):
        """
        After the request confirmation:
        1. Returns money to the customer.
        2. The quantity of products returns to the previous values.
        3. The order status becomes 'Cancelled'.
        4. The object status becomes 'True' (Confirmed).
        """

        order = self.order
        cart = order.cart
        customer = cart.customer
        order_items = cart.items.all()

        total_cost = cart.calculate_sum()
        customer.add_money(total_cost)

        for item in order_items:
            product = item.product
            quantity = item.quantity
            product.increase_quantity(quantity)

        order.cancel()

        self.status = True
        self.save()

    def reject(self):
        """Removes the return order instance if the request is rejected"""

        self.delete()
