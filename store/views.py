from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, Order, OrderItem, Category, Wishlist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category:
        products = products.filter(category__name=category)
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart) if cart else []
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

def remove_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)
    if not items:
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(
        user=request.user,
        total_price=total,
        status="Paid" 
    )
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )
    items.delete()
    return render(request, 'success.html', {'order': order})

def stripe_payment(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/checkout/',
        cancel_url='http://127.0.0.1:8000/cart/',
    )
    return redirect(session.url, code=303)

def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})


def remove_wishlist(request, id):
    Wishlist.objects.filter(id=id).delete()
    return redirect('wishlist')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')