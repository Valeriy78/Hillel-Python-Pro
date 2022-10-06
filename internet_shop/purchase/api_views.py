"""
Purchase application API views
"""

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from internet_shop.serializers import OrderSerializer
from .models import Order


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
