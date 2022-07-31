from django.urls import path
from .views import homepage, product, user_profile


urlpatterns = [
    path('', homepage),
    path('profile', user_profile),
    path('<slug:product>', product),
]
