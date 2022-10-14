"""
My_shop application API views
"""

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from internet_shop.permissions import IsSuperuserOrReadOnly
from internet_shop.serializers import CategorySerializer, ProductSerializer
from .models import Category, Product


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]

