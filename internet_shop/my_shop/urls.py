"""
My_shop application URLConf
"""

from django.urls import path
from my_shop import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='homepage'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),
    path('create/', views.ProductCreateView.as_view(), name='create_product'),
    path('update/<slug:slug>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<slug:slug>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('create-category/', views.CategoryCreateView.as_view(), name='create_category'),
]
