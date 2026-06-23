from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Wishlist
admin.site.register([Product, Category, Cart, CartItem, Order, OrderItem, Wishlist])
