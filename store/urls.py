from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:item_id>/', views.increase_quantity),
    path('decrease/<int:item_id>/', views.decrease_quantity),
    path('remove/<int:item_id>/', views.remove_item),
    path('checkout/', views.checkout, name='checkout'),
    path('stripe-payment/', views.stripe_payment, name='stripe_payment'),
    path('orders/', views.order_history, name='orders'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist),
    path('remove-wishlist/<int:id>/', views.remove_wishlist),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]