"""
My_shop application URLConf
"""

from django.urls import path
from my_shop import api_views, views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='homepage'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),
    path('create/', views.ProductCreateView.as_view(), name='create_product'),
    path('update/<slug:slug>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<slug:slug>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('create-category/', views.CategoryCreateView.as_view(), name='create_category'),
    # API
    path('api/product/', api_views.ProductListCreateAPIView.as_view(), name='api_products'),
    path('api/product/<int:pk>/', api_views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='api_product'),
    path('api/category/', api_views.CategoryListCreateAPIView.as_view(), name='api_categories'),
    path('api/category/<int:pk>/', api_views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='api_category')
]
