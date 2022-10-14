"""
Purchase application API views
"""

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from internet_shop.permissions import IsSuperuserOrReadOnly
from internet_shop.serializers import OrderSerializer
from .models import Order


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]
