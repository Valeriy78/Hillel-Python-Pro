"""
User application API views
"""

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from internet_shop.serializers import UserModelSerializer
from .models import UserModel


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
