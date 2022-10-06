from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from my_shop.models import Category, Product
from purchase.models import Cart, CartItem, Order
from user.models import UserModel


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer implementation"""

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer implementation"""

    class Meta:
        model = Product
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    """User serializer implementation"""

    class Meta:
        model = UserModel
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer implementation"""

    class Meta:
        model = Order
        fields = "__all__"

    def validate_cart(self, cart):
        """
        Check if the shopping cart is empty.
        Check if the customer has enough money.
        """

        if not self.instance:
            cart_items = cart.items.all()
            if cart_items.count() == 0:
                raise serializers.ValidationError("Cart is empty")

            total_cost = cart.calculate_sum()
            if total_cost > cart.customer.money:
                raise serializers.ValidationError("Customer has not enough money!")

        return cart
