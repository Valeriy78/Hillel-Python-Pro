from django.contrib import admin
from .models import Cart, CartItem, Order, OrderReturn

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderReturn)



