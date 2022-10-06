"""
User application URLConf
"""

from django.urls import path
from user import api_views
from .views import user_profile, login_view, logout_view, register_view, deactivate_view, profile_edit_view

urlpatterns = [
    path('profile/', user_profile, name='user'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('deactivate/', deactivate_view, name='deactivate'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    # API
    path('api/user/', api_views.UserListCreateAPIView.as_view(), name='api_users'),
    path('api/user/<int:pk>/', api_views.UserRetrieveUpdateDestroyAPIView.as_view(), name='api_user')
]
