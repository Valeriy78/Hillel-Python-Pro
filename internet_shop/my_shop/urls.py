from django.urls import path
from .views import homepage, product


urlpatterns = [
    path('', homepage, name='homepage'),
    path('product/<slug:product>', product),
]
