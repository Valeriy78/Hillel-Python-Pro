"""
User application API views
"""

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from internet_shop.serializers import UserModelSerializer
from internet_shop.permissions import UserProfilePermission
from .models import UserModel


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
    permission_classes = [UserProfilePermission]


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
    permission_classes = [UserProfilePermission]
