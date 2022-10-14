"""
Purchase application URLConf
"""

from django.urls import path
from purchase import api_views, views


urlpatterns = [
    path('add-to-cart/<slug:slug>/', views.cart_item_create_view, name='add_to_cart'),
    path('delete-from-cart/<int:pk>/', views.cart_item_delete_view, name='delete_from_cart'),
    path('cart-list/', views.cart_list_view, name='cart_list'),
    path('purchase/<int:pk>/', views.purchase_view, name='purchase'),
    path('order-list/', views.order_list_view, name='order_list'),
    path('order/<int:pk>/', views.order_detail_view, name='order'),
    path('return-order/<int:pk>/', views.order_return_request_view, name='return_order'),
    path('return-order-list/', views.order_return_list_view, name='return_order_list'),
    path('return-order-detail/<int:pk>/', views.order_return_detail_view, name='return_order_detail'),
    path('confirm-return-order/<int:pk>/', views.confirm_order_return_view, name='confirm_return_order'),
    # API
    path('api/order/', api_views.OrderListCreateAPIView.as_view(), name='api_orders'),
    path('api/order/<int:pk>/', api_views.OrderRetrieveUpdateDestroyAPIView.as_view(), name='api_order')
]
