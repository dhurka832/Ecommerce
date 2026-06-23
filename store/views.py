from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Wishlist
import stripe
from django.conf import settings

def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products, 'categories': categories,
        'query': query, 'selected_category': category_id
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart_obj)
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f'"{product.name}" added to wishlist!')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, pk):
    item = get_object_or_404(Wishlist, pk=pk, user=request.user)
    item.delete()
    return redirect('wishlist')

@login_required
def checkout(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart_obj)
    total = sum(i.product.price * i.quantity for i in items)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            stripe.Charge.create(amount=int(total * 100), currency='inr', source=token)
            order = Order.objects.create(user=request.user, total_price=total, status='Paid')
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            items.delete()
            return redirect('order_success')
        except stripe.error.StripeError as e:
            messages.error(request, str(e))
    return render(request, 'store/checkout.html', {
        'items': items, 'total': total,
        'stripe_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})
