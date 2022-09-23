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


class CartSerializer(serializers.ModelSerializer):
    """Shopping cart serializer implementation"""

    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    """Cart item serializer implementation"""

    class Meta:
        model = CartItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer implementation"""

    class Meta:
        model = Order
        fields = "__all__"

